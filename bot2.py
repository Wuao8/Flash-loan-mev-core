import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from price_provider import get_market_snapshot

print("CRYPTO OPPORTUNITY ENGINE v1 (SCORING MODE)")

snapshot = get_market_snapshot()
print("SNAPSHOT:", snapshot)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        r = requests.post(url, data=payload, timeout=10)
        print("Telegram status:", r.status_code)
    except Exception as e:
        print("Telegram ERROR:", e)


opportunities = []

# =========================
# SCORING LOOP
# =========================
for token, prices in snapshot.items():

    coinbase = prices["coinbase"]
    dex = prices["dex"]

    print(f"\nTOKEN: {token}")
    print(f"COINBASE: {coinbase}")
    print(f"DEX: {dex}")

    # Spread
    spread = (coinbase - dex) / dex
    spread_pct = abs(spread * 100)

    # SCORE COMPONENTS
    spread_score = min(spread_pct * 50, 100)

    liquidity_score = 70      # placeholder
    stability_score = 60      # placeholder
    cost_penalty = 30         # fees/slippage estimate

    score = (
        spread_score * 0.5 +
        liquidity_score * 0.2 +
        stability_score * 0.2 -
        cost_penalty * 0.1
    )

    score = max(0, min(100, score))

    print(f"SPREAD: {spread_pct:.2f}%")
    print(f"SCORE: {score:.1f}/100")

    opportunities.append({
        "token": token,
        "score": score,
        "spread": spread_pct,
        "binance": coinbase,
        "dex": dex
    })


# =========================
# RANKING TOP OPPORTUNITIES
# =========================
opportunities.sort(key=lambda x: x["score"], reverse=True)
top = opportunities[:3]


msg = "📊 TOP OPPORTUNITIES\n\n"

for i, op in enumerate(top, 1):

    if op["score"] >= 70:
        level = "🔥 STRONG"
    elif op["score"] >= 50:
        level = "⚠️ WEAK"
    else:
        level = "LOW"

    msg += (
        f"{i}. {op['token']}\n"
        f"Score: {op['score']:.1f}/100 ({level})\n"
        f"Spread: {op['spread']:.2f}%\n\n"
    )


print("\n" + msg)
send_telegram(msg)
