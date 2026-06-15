import requests

MEXC_24H_URL = "https://api.mexc.com/api/v3/ticker/24hr"
MEXC_PRICE_URL = "https://api.mexc.com/api/v3/ticker/price"

DEX_TOKEN_URL = "https://api.dexscreener.com/latest/dex/tokens/"

TOP_MARKET_CAP_EXCLUDE = {
    "BTC",
    "ETH",
    "BNB",
    "SOL",
    "XRP",
    "USDT",
    "USDC",
    "DOGE"
}


def safe_float(x):
    try:
        return float(x)
    except:
        return 0


# ------------------------
# MIDCAP LIST
# ------------------------

def get_midcap_symbols(limit=100):

    try:

        r = requests.get(
            MEXC_24H_URL,
            timeout=10
        )

        data = r.json()

        sorted_data = sorted(
            data,
            key=lambda x: float(x.get("quoteVolume", 0)),
            reverse=True
        )

        symbols = []

        for item in sorted_data:

            sym = item.get("symbol", "")

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

        print("LIST ERROR:", e)
        return []


# ------------------------
# MEXC PRICE
# ------------------------

def get_mexc_price(symbol):

    try:

        r = requests.get(
            MEXC_PRICE_URL,
            timeout=10
        )

        data = r.json()

        target = symbol + "USDT"

        for item in data:

            if item.get("symbol") == target:

                return float(
                    item.get("price", 0)
                )

        return None

    except Exception as e:

        print(
            f"MEXC ERROR {symbol}:",
            e
        )

        return None


# ------------------------
# DEX PRICE
# ------------------------

def get_bsc_dex_price(symbol):

    try:

        url = DEX_TOKEN_URL + symbol

        r = requests.get(
            url,
            timeout=10
        )

        data = r.json()

        pairs = data.get("pairs", [])

        if not isinstance(pairs, list):
            return None

        best_price = None
        best_liquidity = 0

        for p in pairs:

            if p.get("chainId") != "bsc":
                continue

            if p.get("dexId") != "pancakeswap":
                continue

            liquidity = safe_float(
                p.get("liquidity", {}).get("usd")
            )

            volume24h = safe_float(
                p.get("volume", {}).get("h24")
            )

            price = safe_float(
                p.get("priceUsd")
            )

            if price <= 0:
                continue

            # filtri più permissivi
            if liquidity < 100000:
                continue

            if volume24h < 25000:
                continue

            if liquidity > best_liquidity:

                best_liquidity = liquidity
                best_price = price

        return best_price

    except Exception as e:

        print(
            f"DEX ERROR {symbol}:",
            e
        )

        return None


# ------------------------
# SNAPSHOT
# ------------------------

def get_market_snapshot():

    snapshot = {}

    symbols = get_midcap_symbols(100)

    print(
        f"SCANNING {len(symbols)} TOKENS..."
    )

    for s in symbols:

        cex = get_mexc_price(s)
        dex = get_bsc_dex_price(s)

        if not cex:
            continue

        if not dex:
            continue

        # anti-follia
        if dex > cex * 3:
            continue

        if dex < cex / 3:
            continue

        snapshot[s] = {
            "cex": cex,
            "dex": dex
        }

        print(
            f"OK {s} | "
            f"CEX={cex} | "
            f"DEX={dex}"
        )

    print(
        f"VALID TOKENS: {len(snapshot)}"
    )

    return snapshot
