import requests

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


def get_market_snapshot():

    snapshot = {}

    try:

        ids = ",".join(TOKENS.values())

        url = f"https://lite-api.jup.ag/price/v3?ids={ids}"

        response = requests.get(url, timeout=10)

        data = response.json()

        for symbol, mint in TOKENS.items():

            if mint in data:

                price = float(data[mint]["usdPrice"])

                snapshot[symbol] = {
                    "orca": price,
                    "raydium": price
                }

        print("LIVE PRICES LOADED")

        return snapshot

    except Exception as e:

        print("JUPITER ERROR:", e)
        print("USING FALLBACK PRICES")

        for symbol, price in MOCK_PRICES.items():

            snapshot[symbol] = {
                "orca": price,
                "raydium": price
            }

        return snapshot
