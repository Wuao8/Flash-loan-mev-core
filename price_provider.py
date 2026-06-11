import requests

MEXC_24H_URL = "https://api.mexc.com/api/v3/ticker/24hr"
MEXC_PRICE_URL = "https://api.mexc.com/api/v3/ticker/price"

DEX_URL = "https://api.dexscreener.com/latest/dex/search?q="

TOP_MARKET_CAP_EXCLUDE = {
    "BTC", "ETH", "BNB", "SOL", "XRP",
    "USDT", "USDC", "DOGE"
}


def get_midcap_symbols(limit=100):

    try:
        r = requests.get(MEXC_24H_URL, timeout=10)
        data = r.json()

        sorted_data = sorted(
            data,
            key=lambda x: float(x.get("quoteVolume", 0)),
            reverse=True
        )

        symbols = []

        for item in sorted_data:

            sym = item["symbol"]

            if not sym.endswith("USDT"):
                continue

            base = sym.replace("USDT", "")

            if base in TOP_MARKET_CAP_EXCLUDE:
                continue

            symbols.append(base)

            if len(symbols) >= limit:
                break

        return symbols

    except Exception as e:
        print("MEXC LIST ERROR:", e)
        return []


def get_mexc_price(symbol):

    try:
        r = requests.get(MEXC_PRICE_URL, timeout=10)
        data = r.json()

        for item in data:

            if item["symbol"] == symbol + "USDT":
                return float(item["price"])

        return None

    except Exception as e:
        print("MEXC PRICE ERROR:", e)
        return None


def get_bsc_dex_price(symbol):

    try:
        r = requests.get(DEX_URL + symbol, timeout=10)
        data = r.json()

        pairs = data.get("pairs", [])

        if not pairs:
            return None

        valid_pairs = []

        for p in pairs:

            chain = p.get("chainId", "")

            liquidity = float(
                p.get("liquidity", {}).get("usd", 0)
            )

            volume24h = float(
                p.get("volume", {}).get("h24", 0)
            )

            quote = p.get(
                "quoteToken", {}
            ).get(
                "symbol", ""
            )

            if chain != "bsc":
                continue

            if liquidity < 500000:
                continue

            if volume24h < 100000:
                continue

            if quote not in ["USDT", "WBNB", "BUSD"]:
                continue

            price = float(
                p.get("priceUsd", 0)
            )

            if price <= 0:
                continue

            valid_pairs.append(
                (price, liquidity)
            )

        if not valid_pairs:
            return None

        best = max(
            valid_pairs,
            key=lambda x: x[1]
        )

        return best[0]

    except Exception as e:
        print("DEX ERROR:", e)
        return None


def get_market_snapshot():

    snapshot = {}

    symbols = get_midcap_symbols(100)

    for s in symbols:

        cex = get_mexc_price(s)
        dex = get_bsc_dex_price(s)

        if not cex or not dex:
            continue

        # sanity check più severo
        if dex > cex * 2:
            continue

        if dex < cex / 2:
            continue

        snapshot[s] = {
            "cex": cex,
            "dex": dex
        }

        print(
            f"OK: {s} | "
            f"CEX={cex:.6f} | "
            f"DEX={dex:.6f}"
        )

    return snapshot
