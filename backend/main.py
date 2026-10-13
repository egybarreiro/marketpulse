from fastapi import FastAPI
from backend.routers.model_router import router as model_router
from backend.routers.ticker_router import router as ticker_router

app = FastAPI()

app.include_router(model_router, prefix="/model")
app.include_router(ticker_router, prefix="/ticker")

@app.get("/")
def root():
    return {"status": "backend ok"}
