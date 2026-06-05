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

    binance = prices["binance"]
    dex = prices["dex"]

    print(f"\nTOKEN: {token}")
    print(f"BINANCE: {binance}")
    print(f"DEX: {dex}")

    # 1. spread base
    spread = (binance - dex) / dex
    spread_pct = abs(spread * 100)

    # 2. scoring factors

    spread_score = min(spread_pct * 40, 100)   # più spread = meglio

    liquidity_score = 70  # placeholder (poi lo rendiamo reale)

    stability_score = 60   # placeholder (poi volatility module)

    cost_penalty = 30      # fee + slippage impatto stimato

    # 3. FINAL SCORE
    score = (
        spread_score * 0.5 +
        liquidity_score * 0.2 +
        stability_score * 0.2 -
        cost_penalty * 0.1
    )

    score = max(0, min(100, score))

    print(f"SPREAD: {spread_pct:.2f}%")
    print(f"SCORE: {score:.1f}/100")

    # 4. decisione
    if score > 70:
        print("🔥 STRONG OPPORTUNITY")
    elif score > 50:
        print("⚠️ WEAK OPPORTUNITY")
    else:
        print("NO TRADE")


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
