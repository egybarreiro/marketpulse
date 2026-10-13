import httpx

API_KEY = "AZ23oC6UXFOc4WGQsereGpi3m3esieJI"

async def fetch_fmp_quotes(symbols: list[str]):
    cleaned = []

    async with httpx.AsyncClient() as client:
        for symbol in symbols:
            url = f"https://financialmodelingprep.com/api/v4/quote-short?symbol={symbol}&apikey={API_KEY}"

            try:
                response = await client.get(url)
                data = response.json()

                if isinstance(data, list) and len(data) > 0:
                    item = data[0]
                    cleaned.append({
                        "symbol": item.get("symbol"),
                        "price": item.get("price"),
                        "change": None,
                    })
            except Exception:
                continue

    return cleaned
