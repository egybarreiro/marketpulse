from fastapi import FastAPI
from routers.ticker_router import router as ticker_router
from routers.model_router import router as model_router

app = FastAPI()

app.include_router(ticker_router, prefix="/ticker")
app.include_router(model_router, prefix="/model")

@app.get("/")
def root():
    return {"message": "MarketPulse API is running"}
