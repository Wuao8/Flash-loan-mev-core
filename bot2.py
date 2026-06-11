from price_provider import get_market_snapshot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import requests

print("CRYPTO ENGINE V3 MIDCAP START")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    })


snapshot = get_market_snapshot()

opportunities = []

for token, prices in snapshot.items():

    cex = prices["cex"]
    dex = prices["dex"]

    spread = abs((cex - dex) / cex) * 100
    
    if spread < 1.5:
        continue
    
    if spread > 15:
        continue
        
    score = spread * 12

    # penalty mega-cap bias already removed upstream
    score = min(score, 100)

    if score < 70:
        continue

    opportunities.append({
        "token": token,
        "score": score,
        "spread": spread,
        "cex": cex,
        "dex": dex
    })

opportunities.sort(key=lambda x: x["score"], reverse=True)

top = opportunities[:3]

if not top:
    print("NO SIGNALS")
    exit()

msg = "🚀 <b>MID-CAP ARB OPPORTUNITIES V3</b>\n\n"

for i, op in enumerate(top, 1):

    msg += (
        f"{i}. <b>{op['token']}</b>\n"
        f"Score: {op['score']:.1f}/100\n"
        f"Spread: {op['spread']:.2f}%\n"
        f"CEX: {op['cex']}\n"
        f"DEX (BSC): {op['dex']}\n\n"
    )

send_telegram(msg)
print(msg)
