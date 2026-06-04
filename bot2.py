import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from price_provider import get_market_snapshot


from price_provider import get_market_snapshot

print("SOLANA ARBITRAGE ENGINE v3 (TELEGRAM ENABLED)")

snapshot = get_market_snapshot()

for token, prices in snapshot.items():

    orca = prices["orca"]
    raydium = prices["raydium"]

    buy = min(orca, raydium)
    sell = max(orca, raydium)

    spread = ((sell - buy) / buy) * 100

    print(f"\nTOKEN: {token}")
    print(f"ORCA: {orca}")
    print(f"RAYDIUM: {raydium}")
    print(f"SPREAD: {spread:.2f}%")

    if spread > 1.0:
        msg = f"""🔥 ARBITRAGE OPPORTUNITY

TOKEN: {token}
ORCA: {orca}
RAYDIUM: {raydium}
SPREAD: {spread:.2f}%"""

        print("SEND:", msg)
        send_telegram(msg)
    else:
        print("NO TRADE")



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
