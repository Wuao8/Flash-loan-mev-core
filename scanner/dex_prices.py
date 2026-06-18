import requests

DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/tokens/"


def safe_float(x):
    try:
        return float(x)
    except:
        return 0.0


def get_token_prices_multi_dex(token_address: str):
    """
    Ritorna lista prezzi da diversi DEX pools su Base
    """
    try:
        r = requests.get(DEXSCREENER_URL + token_address, timeout=10)
        data = r.json()

        pairs = data.get("pairs", [])
        if not pairs:
            return []

        prices = []

        for p in pairs:

            if p.get("chainId") != "base":
                continue

            price = safe_float(p.get("priceUsd"))
            liquidity = safe_float(p.get("liquidity", {}).get("usd"))
            volume = safe_float(p.get("volume", {}).get("h24"))

            if price <= 0:
                continue

            # filtro leggero (NON distruttivo)
            if liquidity < 3000:
                continue

            prices.append({
                "price": price,
                "liquidity": liquidity,
                "volume": volume,
                "dex": p.get("dexId", "unknown")
            })

        return prices

    except Exception as e:
        print("DEX ERROR:", e)
        return []


def get_base_dex_price(token_address: str):
    """
    Prezzo aggregato intelligente + detection mismatch
    """

    prices = get_token_prices_multi_dex(token_address)

    if not prices:
        return None

    # ordina per liquidità (più affidabile)
    prices.sort(key=lambda x: x["liquidity"], reverse=True)

    # prendi top 3 pool per rilevare inefficienze
    top = prices[:3]

    if not top:
        return None

    # prezzo medio pesato (liquidity weighted)
    total_liq = sum(p["liquidity"] for p in top)
    if total_liq == 0:
        return None

    weighted_price = sum(
        p["price"] * p["liquidity"] for p in top
    ) / total_liq

    return weighted_price
