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
        "text": message
    }

    try:
        r = requests.post(url, data=payload, timeout=10)
        print("Telegram status:", r.status_code)
        print("Telegram response:", r.text)
    except Exception as e:
        print("Telegram ERROR:", e)




print("SOLANA ARBITRAGE ENGINE v4 (CLEAN MODE)")

snapshot = get_market_snapshot()

best_trade = None

for token, prices in snapshot.items():

    orca = prices["orca"]
    raydium = prices["raydium"]

    buy = min(orca, raydium)
    sell = max(orca, raydium)

    gross_spread = (sell - buy) / buy

    ORCA_FEE = 0.003
    RAYDIUM_FEE = 0.0025
    SLIPPAGE = 0.002

    net_profit_percent = (gross_spread - ORCA_FEE - RAYDIUM_FEE - SLIPPAGE) * 100

    print(f"\nTOKEN: {token}")
    print(f"NET PROFIT: {net_profit_percent:.2f}%")

    if net_profit_percent > 0.5:

        trade = {
            "token": token,
            "net": net_profit_percent,
            "gross": gross_spread * 100,
            "buy": buy,
            "sell": sell,
            "orca": orca,
            "raydium": raydium
        }

        if best_trade is None or trade["net"] > best_trade["net"]:
            best_trade = trade

    else:
        print("NO TRADE (after fees)")


if best_trade:

    if best_trade["orca"] < best_trade["raydium"]:
        buy_dex = "ORCA"
        sell_dex = "RAYDIUM"
    else:
        buy_dex = "RAYDIUM"
        sell_dex = "ORCA"

    msg = (
        "TOP ARBITRAGE SIGNAL\n\n"
        f"TOKEN: {best_trade['token']}\n\n"
        f"BUY ON: {buy_dex}\n"
        f"SELL ON: {sell_dex}\n\n"
        f"NET PROFIT: {best_trade['net']:.2f}%\n"
        f"GROSS SPREAD: {best_trade['gross']:.2f}%\n\n"
        f"BUY PRICE: {best_trade['buy']}\n"
        f"SELL PRICE: {best_trade['sell']}"
    )

    print("\nSEND BEST SIGNAL")
    send_telegram(msg)

else:
    print("\nNO GOOD OPPORTUNITIES")
