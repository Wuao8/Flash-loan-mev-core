import requests

# =========================
# CEX SOURCE (WORKING GLOBAL)
# =========================
COINBASE_URL = "https://api.coinbase.com/v2/prices"

# =========================
# TOKEN CONFIG (CEX vs DEX)
# =========================
TOKENS = {
    "BNB": {
        "cex": "BNB-USD",
        "dexscreener": "wbnb"
    },
    "CAKE": {
        "cex": "CAKE-USD",
        "dexscreener": "pancakeswap"
    },
    "ETH": {
        "cex": "ETH-USD",
        "dexscreener": "ethereum"
    }
}

# -----------------------------
# CEX PRICE (BINANCE)
# -----------------------------
def get_coinbase_price(symbol):
    try:
        url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
        r = requests.get(url, timeout=10)
        data = r.json()
        return float(data["data"]["amount"])
    except Exception as e:
        print("COINBASE ERROR:", e)
        return None


# -----------------------------
# DEX PRICE (DEXSCREENER / PANCAKE)
# -----------------------------
def get_dex_price(query):
    """
    Uses DexScreener as proxy for PancakeSwap/BSC liquidity pools
    """
    try:
        url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
        r = requests.get(url, timeout=10)
        data = r.json()

        pairs = data.get("pairs", [])
        if not pairs:
            return None

        # take most liquid pair
        best = pairs[0]
        return float(best["priceUsd"])

    except Exception as e:
        print("DEX ERROR:", e)
        return None


# -----------------------------
# SNAPSHOT ENGINE
# -----------------------------
def get_market_snapshot():

    snapshot = {}

    for token, data in TOKENS.items():

        cex_price = get_coinbase_price("BTC")
        dex_price = get_dex_price(data["dexscreener"])


        print(f"{token} CEX:", cex_price)
        print(f"{token} DEX:", dex_price)

        if cex_price is None or dex_price is None:
            print(f"SKIP {token} (missing data)")
            continue

        snapshot[token] = {
            "cex": cex_price,
            "dex": dex_price
}

    print("BNB CEX vs DEX SNAPSHOT READY")

    return snapshot
