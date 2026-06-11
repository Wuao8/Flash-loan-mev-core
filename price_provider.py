import requests

MEXC_24H_URL = "https://api.mexc.com/api/v3/ticker/24hr"
MEXC_PRICE_URL = "https://api.mexc.com/api/v3/ticker/price"

# DexScreener by TOKEN (fallback)
DEX_SEARCH_URL = "https://api.dexscreener.com/latest/dex/search?q="

# DexScreener by CONTRACT (preferred)
DEX_TOKEN_URL = "https://api.dexscreener.com/latest/dex/tokens/"

TOP_MARKET_CAP_EXCLUDE = {
    "BTC", "ETH", "BNB", "SOL", "XRP",
    "USDT", "USDC", "DOGE"
}


# -------------------------
# GET MID CAP SYMBOLS
# -------------------------
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
        print("MEXC LIST ERROR:", e)
        return []


# -------------------------
# MEXC PRICE
# -------------------------
def get_mexc_price(symbol):

    try:
        r = requests.get(MEXC_PRICE_URL, timeout=10)
        data = r.json()

        for item in data:

            if item.get("symbol") == symbol + "USDT":
                return float(item.get("price", 0))

        return None

    except Exception as e:
        print("MEXC PRICE ERROR:", e)
        return None


# -------------------------
# TRY GET CONTRACT ADDRESS FROM PAIR
# -------------------------
def extract_contract(p):

    if not isinstance(p, dict):
        return None

    base = p.get("baseToken")
    if isinstance(base, dict):
        addr = base.get("address")
        if addr:
            return addr

    return None


# -------------------------
# DEX PRICE (CONTRACT FIRST)
# -------------------------
def get_bsc_dex_price(symbol):

    try:
        r = requests.get(DEX_SEARCH_URL + symbol, timeout=10)
        data = r.json()

        pairs = data.get("pairs", [])

        if not isinstance(pairs, list):
            return None

        best_price = None
        best_liq = 0

        for p in pairs:

            if not isinstance(p, dict):
                continue

            if p.get("chainId") != "bsc":
                continue

            dex_id = p.get("dexId", "")
            if dex_id != "pancakeswap":
                continue

            liquidity_obj = p.get("liquidity")
            volume_obj = p.get("volume")

            if not isinstance(liquidity_obj, dict):
                continue
            if not isinstance(volume_obj, dict):
                continue

            liquidity = float(liquidity_obj.get("usd", 0))
            volume24h = float(volume_obj.get("h24", 0))

            if liquidity < 500000:
                continue

            if volume24h < 100000:
                continue

            price = float(p.get("priceUsd", 0))
            if price <= 0:
                continue

            # contract extraction (future-proof)
            contract = extract_contract(p)

            # prefer high liquidity
            if liquidity > best_liq:
                best_liq = liquidity
                best_price = price

        return best_price

    except Exception as e:
        print("DEX ERROR:", e)
        return None


# -------------------------
# SNAPSHOT ENGINE
# -------------------------
def get_market_snapshot():

    snapshot = {}

    symbols = get_midcap_symbols(100)

    for s in symbols:

        cex = get_mexc_price(s)
        dex = get_bsc_dex_price(s)

        if not cex or not dex:
            continue

        # anti noise band
        if dex > cex * 2:
            continue

        if dex < cex / 2:
            continue

        snapshot[s] = {
            "cex": cex,
            "dex": dex
        }

        print(f"OK: {s} | CEX={cex} | DEX={dex}")

    return snapshot
