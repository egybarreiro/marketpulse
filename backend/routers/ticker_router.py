from fastapi import APIRouter
from backend.services.alpha_service import fetch_alpha_quotes
from backend.services.fmp_service import fetch_fmp_quotes


router = APIRouter(prefix="/ticker", tags=["ticker"])

@router.get("/")
async def get_ticker():
    symbols = [
        "AAPL","MSFT","GOOGL","AMZN","NVDA","TSLA","META","NFLX","AMD","INTC",
        "JPM","BAC","WFC","GS","C","V","MA","PYPL","SHOP",
        "KO","PEP","MCD","SBUX","WMT","COST","HD","TGT","LOW","DIS",
        "NKE","TSM","QCOM","AVGO","ORCL","CRM","ADBE","IBM","CSCO","UBER",
        "XOM","CVX","PFE","MRK","ABBV","TMO","UNH","UPS","FDX","GE"
    ]

    quotes = await fetch_alpha_quotes(symbols)

    cleaned = []
    for item in quotes:
        if item.get("price") is None:
            continue
        if item["price"] == 0:
            continue
        cleaned.append(item)

    return {"data": cleaned}
