from price_provider import get_market_snapshot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import requests

print("CRYPTO ENGINE V4 START")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "HTML"
        },
        timeout=10
    )


snapshot = get_market_snapshot()

opportunities = []

for token, prices in snapshot.items():

    cex = prices["cex"]
    dex = prices["dex"]

    spread = abs((cex - dex) / cex) * 100

    print(
        f"{token} | "
        f"CEX={cex:.8f} | "
        f"DEX={dex:.8f} | "
        f"SPREAD={spread:.2f}%"
    )

    # filtro minimo realistico
    if spread < 1.0:
        continue

    # evita anomalie gigantesche
    if spread > 20:
        continue

    opportunities.append({
        "token": token,
        "spread": spread,
        "cex": cex,
        "dex": dex
    })

opportunities.sort(
    key=lambda x: x["spread"],
    reverse=True
)

top = opportunities[:5]

if not top:
    print("NO SIGNALS")
    exit()

msg = "🚀 <b>BSC ↔ MEXC SPREAD MONITOR</b>\n\n"

for i, op in enumerate(top, start=1):

    direction = (
        "BUY DEX → SELL CEX"
        if op["dex"] < op["cex"]
        else
        "BUY CEX → SELL DEX"
    )

    msg += (
        f"{i}. <b>{op['token']}</b>\n"
        f"Spread: {op['spread']:.2f}%\n"
        f"{direction}\n"
        f"CEX: {op['cex']:.8f}\n"
        f"DEX: {op['dex']:.8f}\n\n"
    )

send_telegram(msg)

print(msg)
