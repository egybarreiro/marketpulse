import pandas as pd
import numpy as np
import yfinance as yf
from xgboost import XGBRegressor
import os

# Tickers oficiales del LMS Terminal34 + SPY + VIX
TICKERS = [
    "AAPL", "MSFT", "NVDA", "AMZN",
    "GOOGL", "JPM", "XOM", "JNJ",
    "SPY", "^VIX"
]

START_DATE = "2010-01-01"
END_DATE = "2024-12-31"


def download_data():
    frames = []
    for t in TICKERS:
        print(f"⬇️ Descargando {t}...")
        df = yf.download(t, start=START_DATE, end=END_DATE)

        # Asegurar columnas planas
        df = df.copy()
        df.columns = [c if isinstance(c, str) else c[0] for c in df.columns]

        df["ticker"] = t
        frames.append(df)

    data = pd.concat(frames)
    data = data.dropna()
    return data


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["ticker", "Date"])

    # Usamos Close en vez de Adj Close (VIX no tiene Adj Close)
    close = df["Close"]

    df["return_1d"] = df.groupby("ticker")["Close"].pct_change(1)
    df["return_5d"] = df.groupby("ticker")["Close"].pct_change(5)

    df["sma_20"] = df.groupby("ticker")["Close"].transform(lambda x: x.rolling(20).mean())
    df["ema_50"] = df.groupby("ticker")["Close"].transform(lambda x: x.ewm(span=50).mean())

    df["vol_20"] = df.groupby("ticker")["return_1d"].transform(lambda x: x.rolling(20).std())

    df = df.dropna()
    return df


def build_dataset(df: pd.DataFrame):
    # Target: retorno futuro 1 día
    df["target_return_1d_future"] = df.groupby("ticker")["return_1d"].shift(-1)
    df = df.dropna()

    feature_cols = [
        "return_1d", "return_5d",
        "sma_20", "ema_50", "vol_20",
        "Volume"
    ]

    X = df[feature_cols].values
    y = df["target_return_1d_future"].values

    return X, y, feature_cols


def train_model(X, y):
    model = XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        n_jobs=-1
    )
    print("🤖 Entrenando modelo...")
    model.fit(X, y)
    return model


def save_model_json(model, path="backend/colab/model_return_1d.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    model.save_model(path)
    print(f"💾 Modelo guardado en: {path}")


if __name__ == "__main__":
    print("⬇️ Descargando datos...")
    df = download_data()

    print("🧮 Generando features...")
    df = add_features(df)

    print("📦 Construyendo dataset...")
    X, y, feature_cols = build_dataset(df)

    print("🤖 Entrenando modelo...")
    model = train_model(X, y)

    print("💾 Guardando modelo en formato JSON...")
    save_model_json(model)

    print("✅ Pipeline de entrenamiento completado.")
