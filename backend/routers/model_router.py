from fastapi import APIRouter
import joblib

router = APIRouter()

# Load regression and classification models
regression_model = joblib.load("colab/regression_model.pkl")
classification_model = joblib.load("colab/classification_model.pkl")

@router.post("/predict-regression")
async def predict_regression(payload: dict):
    x = payload["features"]
    y = regression_model.predict([x])[0]
    return {"prediction": float(y)}

@router.post("/predict-classification")
async def predict_classification(payload: dict):
    x = payload["features"]
    y = classification_model.predict([x])[0]
    return {"prediction": str(y)}
