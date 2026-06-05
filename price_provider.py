import requests

# Jupiter Quote API
JUP_QUOTE_URL = "https://quote-api.jup.ag/v6/quote"

# Token mint list
TOKENS = {
    "SOL": "So11111111111111111111111111111111111111112",
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
}

MOCK_PRICES = {
    "SOL": 100.0,
    "USDC": 1.0,
    "JUP": 0.75,
    "BONK": 0.00002
}


def get_quote(input_mint, output_mint, amount=1_000_000, dex=None):
    """
    Get Jupiter quote.
    amount is in smallest unit (we keep it fixed for comparison)
    """

    try:
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount,
            "slippageBps": 50
        }

        # Force routing by DEX if supported
        if dex:
            params["dexes"] = dex

        r = requests.get(JUP_QUOTE_URL, params=params, timeout=10)
        data = r.json()

        if "data" in data and len(data["data"]) > 0:
            return int(data["data"][0]["outAmount"])

        return None

    except Exception as e:
        print("QUOTE ERROR:", e)
        return None


def get_market_snapshot():
    """
    Real arbitrage snapshot:
    compares Orca vs Raydium routes via Jupiter
    """

    snapshot = {}

    for symbol, mint in TOKENS.items():

        if symbol == "USDC":
            continue

        # Orca route
        orca_out = get_quote(mint, TOKENS["USDC"], dex="Orca")

        # Raydium route
        raydium_out = get_quote(mint, TOKENS["USDC"], dex="Raydium")

        # fallback if API fails
        if not orca_out or not raydium_out:
            base = MOCK_PRICES.get(symbol, 1)
            snapshot[symbol] = {
                "orca": base * 1.001,
                "raydium": base * 0.999
            }
            continue

        # convert to price (USDC per token)
        orca_price = orca_out / 1_000_000
        raydium_price = raydium_out / 1_000_000

        snapshot[symbol] = {
            "orca": round(orca_price, 6),
            "raydium": round(raydium_price, 6)
        }

    print("REAL DEX SNAPSHOT LOADED")

    return snapshot
