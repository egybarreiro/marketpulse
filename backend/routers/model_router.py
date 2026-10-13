from fastapi import APIRouter
import joblib

router = APIRouter()

# Cargar modelos correctos desde la carpeta colab/
regression_model = joblib.load("colab/model_reg.pkl")
classification_model = joblib.load("colab/model_clf.pkl")
scaler = joblib.load("colab/scaler.pkl")

@router.post("/predict-regression")
async def predict_regression(payload: dict):
    x = payload["features"]
    x_scaled = scaler.transform([x])
    y = regression_model.predict(x_scaled)[0]
    return {"prediction": float(y)}

@router.post("/predict-classification")
async def predict_classification(payload: dict):
    x = payload["features"]
    x_scaled = scaler.transform([x])
    y = classification_model.predict(x_scaled)[0]
    return {"prediction": str(y)}
