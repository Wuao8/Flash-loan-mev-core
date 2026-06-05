import requests

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"

# Token list (CEX symbol + DEX Screener query)
TOKENS = {
    "BNB": {
        "binance": "BNBUSDT",
        "dexscreener": "wbnb"
    },
    "CAKE": {
        "binance": "CAKEUSDT",
        "dexscreener": "pancakeswap"
    },
    "ETH": {
        "binance": "ETHUSDT",
        "dexscreener": "ethereum"
    }
}


# -----------------------------
# CEX PRICE (BINANCE)
# -----------------------------
def get_binance_price(symbol):
    try:
        r = requests.get(BINANCE_URL, params={"symbol": symbol}, timeout=10)
        data = r.json()

        price = data.get("price")

        if price is None:
            print("BINANCE BAD RESPONSE:", data)
            return None

        return float(price)

    except Exception as e:
        print("BINANCE ERROR:", e)
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

        binance_price = get_binance_price(data["binance"])
        dex_price = get_dex_price(data["dexscreener"])

        if binance_price is None or dex_price is None:
            print(f"SKIP {token} (missing data)")
            continue

        snapshot[token] = {
            "binance": binance_price,
            "dex": dex_price
        }

    print("BNB CEX vs DEX SNAPSHOT READY")

    return snapshot
