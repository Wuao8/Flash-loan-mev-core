import requests

TOKENS = {
    "SOL": "SOLUSDT",
    "JUP": "JUPUSDT",
    "BONK": "BONKUSDT"
}

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"

JUPITER_PRICE_URL = "https://price.jup.ag/v4/price"

def get_binance_price(symbol):
    try:
        r = requests.get(BINANCE_URL, params={"symbol": symbol}, timeout=10)
        data = r.json()
        return float(data["price"])
    except Exception as e:
        print("BINANCE ERROR:", e)
        return None


def get_jupiter_price(mint):
    try:
        r = requests.get(JUPITER_PRICE_URL, params={"ids": mint}, timeout=10)
        data = r.json()
        return float(data["data"][mint]["price"])
    except Exception as e:
        print("JUPITER ERROR:", e)
        return None


# mint list Solana
MINTS = {
    "SOL": "So11111111111111111111111111111111111111112",
    "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
}


def get_market_snapshot():
    snapshot = {}

    for symbol in TOKENS.keys():

        binance_price = get_binance_price(TOKENS[symbol])
        jupiter_price = get_jupiter_price(MINTS[symbol])

        if not binance_price or not jupiter_price:
            continue

        snapshot[symbol] = {
            "binance": binance_price,
            "dex": jupiter_price
        }

    print("CEX vs DEX SNAPSHOT LOADED")

    return snapshot
