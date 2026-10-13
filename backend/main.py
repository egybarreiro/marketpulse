from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.ticker_router import router as ticker_router

app = FastAPI(title="MarketPulse Backend")

# ============================
# CORS — NECESARIO PARA LIVE SERVER
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Permite llamadas desde 5500, 5501, etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "backend ok"}

# Registrar rutas
app.include_router(ticker_router)
