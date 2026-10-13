from fastapi import APIRouter
import yfinance as yf
import pandas as pd
import numpy as np
from xgboost import XGBRegressor

router = APIRouter(
    prefix="",
    tags=["model"]
)

MODEL_PATH = "backend/colab/model_return_1d.json"


# ============================
# CARGA DEL MODELO
# ============================

def load_model_safe() -> XGBRegressor | None:
    """Carga el modelo XGBoost desde JSON de forma segura."""
    try:
        model = XGBRegressor()
        model.load_model(MODEL_PATH)
        return model
    except Exception as e:
        print(f"⚠️ Error cargando modelo JSON: {e}")
        return None


# ============================
# FEATURE ENGINEERING
# ============================

def compute_features(df: pd.DataFrame) -> np.ndarray | None:
    """Genera el vector de features para predicción."""
    try:
        df = df.copy()
        df = df.sort_values("Date")

        # Features base
        df["return_1d"] = df["Close"].pct_change(1)
        df["return_5d"] = df["Close"].pct_change(5)
        df["sma_20"] = df["Close"].rolling(20).mean()
        df["ema_50"] = df["Close"].ewm(span=50).mean()
        df["vol_20"] = df["return_1d"].rolling(20).std()

        # ============================
        # INDICADORES TÉCNICOS AVANZADOS
        # ============================

        # RSI 14
        delta = df["Close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        df["rsi_14"] = 100 - (100 / (1 + rs))

        # MACD
        ema12 = df["Close"].ewm(span=12).mean()
        ema26 = df["Close"].ewm(span=26).mean()
        df["macd"] = ema12 - ema26
        df["signal_macd"] = df["macd"].ewm(span=9).mean()

        # Momentum
        df["momentum_10"] = df["Close"].pct_change(10)

        df = df.dropna()

        feature_cols = [
            "return_1d", "return_5d",
            "sma_20", "ema_50", "vol_20",
            "Volume",
            "rsi_14", "macd", "signal_macd", "momentum_10"
        ]

        return df[feature_cols].iloc[-1].values

    except Exception as e:
        print(f"⚠️ Error generando features: {e}")
        return None


# ============================
# SEÑALES AVANZADAS
# ============================

def generate_signal(pred: float) -> str:
    """Genera señal avanzada BUY/SELL STRONG."""
    if pred > 0.03:
        return "BUY STRONG"
    if pred > 0.01:
        return "BUY"
    if pred < -0.03:
        return "SELL STRONG"
    if pred < -0.01:
        return "SELL"
    return "HOLD"


# ============================
# ENDPOINT: PREDICCIÓN SIMPLE
# ============================

@router.get("/predict-regression/{ticker}")
async def predict_regression(ticker: str):
    """Predice retorno 1 día usando el modelo entrenado."""
    model = load_model_safe()
    if model is None:
        return {"status": "error", "message": "Modelo no disponible"}

    df = yf.download(ticker, period="1y")
    if df.empty:
        return {"status": "error", "message": "Ticker no encontrado"}

    X = compute_features(df)
    if X is None:
        return {"status": "error", "message": "No se pudieron generar features"}

    try:
        pred = float(model.predict(X.reshape(1, -1))[0])
        signal = generate_signal(pred)

        last_close = float(df["Close"].iloc[-1])
        future_price = last_close * (1 + pred)

        return {
            "status": "ok",
            "ticker": ticker.upper(),
            "prediction_return_1d": pred,
            "future_price": future_price,
            "signal": signal
        }

    except Exception as e:
        return {"status": "error", "message": f"Error generando predicción: {e}"}


# ============================
# ENDPOINT: ANÁLISIS COMPLETO
# ============================

@router.get("/analyze/{ticker}")
async def analyze_ticker(ticker: str):
    """Análisis técnico + predicción + señal + indicadores avanzados."""
    model = load_model_safe()
    if model is None:
        return {"status": "error", "message": "Modelo no disponible"}

    df = yf.download(ticker, period="1y")
    if df.empty:
        return {"status": "error", "message": "Ticker no encontrado"}

    X = compute_features(df)
    if X is None:
        return {"status": "error", "message": "No se pudieron generar features"}

    try:
        pred = float(model.predict(X.reshape(1, -1))[0])
        signal = generate_signal(pred)

        last_close = float(df["Close"].iloc[-1])
        future_price = last_close * (1 + pred)

        # Indicadores técnicos
        rsi_14 = float(df["rsi_14"].iloc[-1])
        macd = float(df["macd"].iloc[-1])
        signal_macd = float(df["signal_macd"].iloc[-1])
        momentum_10 = float(df["momentum_10"].iloc[-1])

        sma_20 = float(df["Close"].rolling(20).mean().iloc[-1])
        ema_50 = float(df["Close"].ewm(span=50).mean().iloc[-1])

        return {
            "status": "ok",
            "ticker": ticker.upper(),
            "last_close": last_close,
            "future_price": future_price,
            "sma_20": sma_20,
            "ema_50": ema_50,
            "prediction_return_1d": pred,
            "signal": signal,

            # Indicadores avanzados
            "rsi_14": rsi_14,
            "macd": macd,
            "signal_macd": signal_macd,
            "momentum_10": momentum_10
        }

    except Exception as e:
        return {"status": "error", "message": f"Error en análisis: {e}"}
