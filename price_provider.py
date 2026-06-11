import requests

MEXC_24H_URL = "https://api.mexc.com/api/v3/ticker/24hr"
MEXC_PRICE_URL = "https://api.mexc.com/api/v3/ticker/price"

# DexScreener contract-first (PRIMARIO)
DEX_TOKEN_URL = "https://api.dexscreener.com/latest/dex/tokens/"

TOP_MARKET_CAP_EXCLUDE = {
    "BTC", "ETH", "BNB", "SOL", "XRP",
    "USDT", "USDC", "DOGE"
}


# -----------------------------
# MID CAP UNIVERSE
# -----------------------------
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


# -----------------------------
# MEXC PRICE
# -----------------------------
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


# -----------------------------
# SAFE DEX PARSER
# -----------------------------
def safe_float(x):
    try:
        return float(x)
    except:
        return 0


# -----------------------------
# CONTRACT-FIRST DEX PRICE
# -----------------------------
def get_bsc_dex_price(symbol):

    try:
        r = requests.get(DEX_TOKEN_URL + symbol, timeout=10)
        data = r.json()

        pairs = data.get("pairs", [])

        if not isinstance(pairs, list):
            return None

        seen_contracts = set()
        best_price = None
        best_liquidity = 0

        for p in pairs:

            if not isinstance(p, dict):
                continue

            if p.get("chainId") != "bsc":
                continue

            if p.get("dexId") != "pancakeswap":
                continue

            base_token = p.get("baseToken", {})
            if not isinstance(base_token, dict):
                continue

            contract = base_token.get("address")
            if not contract:
                continue

            # ❌ remove duplicates (CLO fix)
            if contract in seen_contracts:
                continue
            seen_contracts.add(contract)

            liquidity_obj = p.get("liquidity", {})
            volume_obj = p.get("volume", {})

            if not isinstance(liquidity_obj, dict):
                continue
            if not isinstance(volume_obj, dict):
                continue

            liquidity = safe_float(liquidity_obj.get("usd"))
            volume24h = safe_float(volume_obj.get("h24"))

            if liquidity < 500000:
                continue

            if volume24h < 100000:
                continue

            price = safe_float(p.get("priceUsd"))
            if price <= 0:
                continue

            # pick best liquidity pool ONLY
            if liquidity > best_liquidity:
                best_liquidity = liquidity
                best_price = price

        return best_price

    except Exception as e:
        print("DEX ERROR:", e)
        return None


# -----------------------------
# SNAPSHOT ENGINE
# -----------------------------
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
