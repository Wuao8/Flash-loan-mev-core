import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from price_provider import get_market_snapshot

print("CRYPTO OPPORTUNITY ENGINE v1 (SCORING MODE)")

snapshot = get_market_snapshot()
print("SNAPSHOT:", snapshot)


for token, prices in snapshot.items():

    cex = prices["cex"]
    dex = prices["dex"]

    if cex is None or dex is None:
        continue

    if cex < dex:
        buy = "CEX (Coinbase)"
        sell = "DEX (Pancake via DexScreener)"
    else:
        buy = "DEX (Pancake via DexScreener)"
        sell = "CEX (Coinbase)"

    spread = abs((dex - cex) / cex) * 100

    score = min(spread * 20, 100)  # placeholder coerente

    msg = (
        f"🚨 <b>TOP OPPORTUNITY</b>\n\n"
        f"<b>TOKEN:</b> {token}\n\n"
        f"<b>BUY ON:</b> {buy}\n"
        f"<b>SELL ON:</b> {sell}\n\n"
        f"<b>CEX PRICE:</b> {cex}\n"
        f"<b>DEX PRICE:</b> {dex}\n\n"
        f"<b>SPREAD:</b> {spread:.2f}%\n"
        f"<b>SCORE:</b> {score:.1f}/100\n"
    )

    send_telegram(msg)



# =========================
# SCORING LOOP
# =========================
for token, prices in snapshot.items():

    cex = prices["cex"]
    dex = prices["dex"]

    print(f"\nTOKEN: {token}")
    print(f"CEX: {cex}")
    print(f"DEX: {dex}")

    # Spread
    spread = (cex - dex) / dex
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
        "cex": cex,
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
