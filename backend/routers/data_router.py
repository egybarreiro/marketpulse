from fastapi import APIRouter, UploadFile, File
import pandas as pd

router = APIRouter(
    prefix="",
    tags=["data"]
)

@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Recibe un archivo CSV, lo carga con pandas y devuelve info básica.
    """
    try:
        df = pd.read_csv(file.file)

        return {
            "status": "ok",
            "message": "Dataset recibido correctamente.",
            "rows": len(df),
            "columns": list(df.columns)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error procesando dataset: {e}"
        }


@router.get("/analyze/{ticker}")
async def analyze_ticker(ticker: str):
    """
    Recibe un ticker (ej: AAPL) y devuelve un placeholder.
    """
    return {
        "status": "ok",
        "ticker": ticker.upper(),
        "message": "Endpoint listo para conectar modelos y análisis real."
    }
