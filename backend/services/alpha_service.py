import yfinance as yf
import time

TTL = 10  # refresco cada 10 segundos

CACHE = {}


async def fetch_alpha_quotes(symbols: list[str]):
    current_time = time.time()
    cleaned = []

    for symbol in symbols:

        # Inicializar cache si no existe
        if symbol not in CACHE:
            CACHE[symbol] = {
                "timestamp": 0,
                "data": {
                    "symbol": symbol,
                    "price": 0.0,
                    "change": 0.0
                }
            }

        # Usar cache si está fresco
        if current_time - CACHE[symbol]["timestamp"] < TTL:
            cleaned.append(CACHE[symbol]["data"])
            continue

        try:
            ticker = yf.Ticker(symbol)

            # FAST INFO → instantáneo, sin SQ, sin history lento
            info = ticker.fast_info

            price = info.last_price
            open_price = info.open

            if price is None or open_price is None:
                cleaned.append(CACHE[symbol]["data"])
                continue

            change = price - open_price

            entry = {
                "symbol": symbol,
                "price": float(price),
                "change": float(change)
            }

            CACHE[symbol] = {
                "timestamp": current_time,
                "data": entry
            }

            cleaned.append(entry)

        except Exception:
            cleaned.append(CACHE[symbol]["data"])

    return cleaned
