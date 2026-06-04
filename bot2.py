import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from price_provider import get_market_snapshot


from price_provider import get_market_snapshot

print("SOLANA ARBITRAGE ENGINE v3 (TELEGRAM ENABLED)")

snapshot = get_market_snapshot()


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print("Telegram error:", e)

for token, prices in snapshot.items():

    orca = prices["orca"]
    raydium = prices["raydium"]

    buy = min(orca, raydium)
    sell = max(orca, raydium)

    gross_spread = (sell - buy) / buy

    # --- COSTI REALISTICI ---
    ORCA_FEE = 0.003
    RAYDIUM_FEE = 0.0025
    SLIPPAGE = 0.002

    total_fees = ORCA_FEE + RAYDIUM_FEE + SLIPPAGE

    net_profit = gross_spread - total_fees
    net_profit_percent = net_profit * 100

    print(f"\nTOKEN: {token}")
    print(f"ORCA: {orca}")
    print(f"RAYDIUM: {raydium}")
    print(f"GROSS SPREAD: {gross_spread*100:.2f}%")
    print(f"NET PROFIT: {net_profit_percent:.2f}%")

    if net_profit_percent > 0.5:
        msg = f""" NET ARBITRAGE OPPORTUNITY

if orca < raydium:
    buy_dex = "ORCA"
    sell_dex = "RAYDIUM"
else:
    buy_dex = "RAYDIUM"
    sell_dex = "ORCA"

msg = f""" NET ARBITRAGE OPPORTUNITY

TOKEN: {token}

BUY ON: {buy_dex}
SELL ON: {sell_dex}

NET PROFIT: {net_profit_percent:.2f}%
GROSS SPREAD: {gross_spread*100:.2f}%

BUY PRICE: {buy}
SELL PRICE: {sell}"""




