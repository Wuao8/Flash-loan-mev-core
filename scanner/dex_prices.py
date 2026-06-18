import requests

DEXSCREENER_TOKEN_URL = "https://api.dexscreener.com/latest/dex/tokens/"


def safe_float(x):
    try:
        return float(x)
    except:
        return 0.0


def get_base_dex_price(token_address: str):
    try:
        url = DEXSCREENER_TOKEN_URL + token_address
        r = requests.get(url, timeout=10)
        data = r.json()

        pairs = data.get("pairs", [])
        if not pairs:
            return None

        prices = []

        for p in pairs:

            if p.get("chainId") != "base":
                continue

            price = safe_float(p.get("priceUsd"))
            liquidity = safe_float(p.get("liquidity", {}).get("usd"))

            if price <= 0:
                continue

            # filtro MOLTO più soft (importante per debug)
            if liquidity < 5000:
                continue

            prices.append(price)

        if not prices:
            return None

        # invece di best liquidity → media robusta
        return sum(prices) / len(prices)

    except Exception as e:
        print("DEX ERROR:", e)
        return None
