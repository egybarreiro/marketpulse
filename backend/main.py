from fastapi import FastAPI
from backend.routers.model_router import router as model_router
from backend.routers.ticker_router import router as ticker_router
from backend.routers.data_router import router as data_router  # ⬅ NUEVO

app = FastAPI()

# Routers existentes
app.include_router(model_router, prefix="/model")
app.include_router(ticker_router, prefix="/ticker")

# Nuevo router para datasets y análisis por ticker
app.include_router(data_router, prefix="/data")

@app.get("/")
def root():
    return {"status": "backend ok"}
