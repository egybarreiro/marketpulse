from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.routers.model_router import router as model_router
from backend.routers.ticker_router import router as ticker_router
from backend.routers.data_router import router as data_router

app = FastAPI()

# Routers primero
app.include_router(model_router, prefix="/model")
app.include_router(ticker_router, prefix="/ticker")
app.include_router(data_router, prefix="/data")

# Frontend al final
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
