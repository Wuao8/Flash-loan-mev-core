print("SOLANA ARBITRAGE ENGINE v0")

# --- MOCK PRICES (fase 1) ---
orca_prices = {
    "SOL": 100.0,
    "JUP": 0.75,
    "BONK": 0.00002
}

raydium_prices = {
    "SOL": 101.2,
    "JUP": 0.78,
    "BONK": 0.000021
}

# --- ENGINE ---
def calculate_spread(token):
    buy = min(orca_prices[token], raydium_prices[token])
    sell = max(orca_prices[token], raydium_prices[token])

    spread = ((sell - buy) / buy) * 100

    return buy, sell, spread

# --- ANALYSIS ---
for token in orca_prices.keys():
    buy, sell, spread = calculate_spread(token)

    print(f"\nTOKEN: {token}")
    print(f"BUY PRICE: {buy}")
    print(f"SELL PRICE: {sell}")
    print(f"SPREAD: {spread:.2f}%")

    if spread > 1.0:
        print("🔥 OPPORTUNITÀ INTERESSANTE")
    else:
        print("❌ NO TRADE")
