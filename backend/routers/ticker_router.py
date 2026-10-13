from fastapi import APIRouter
from ..services.alpha_service import fetch_alpha_quotes

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

    # Obtener cotizaciones
    quotes = await fetch_alpha_quotes(symbols)

    # ============================
    # FILTRO DE SIMBOLOS MUERTOS
    # ============================
    cleaned = []
    for item in quotes:
        # Filtrar símbolos sin precio
        if item.get("price") is None:
            continue

        # Filtrar precios inválidos
        if item["price"] == 0:
            continue

        cleaned.append(item)

    return {"data": cleaned}
