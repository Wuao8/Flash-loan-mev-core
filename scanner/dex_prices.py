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
        if not isinstance(pairs, list):
            return None

        best_price = None
        best_liquidity = 0

        for p in pairs:

            if p.get("chainId") != "base":
                continue

            liquidity = safe_float(p.get("liquidity", {}).get("usd"))
            volume = safe_float(p.get("volume", {}).get("h24"))
            price = safe_float(p.get("priceUsd"))

            if price <= 0:
                continue

            if liquidity < 50000:
                continue

            if volume < 20000:
                continue

            if liquidity > best_liquidity:
                best_liquidity = liquidity
                best_price = price

        return best_price

    except Exception as e:
        print("DEX ERROR:", e)
        return None
