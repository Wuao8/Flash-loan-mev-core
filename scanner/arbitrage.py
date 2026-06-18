def find_opportunity(symbol, cex_price, dex_price):

    if not cex_price or not dex_price:
        return None

    spread = ((dex_price - cex_price) / cex_price) * 100

    direction = "DEX->CEX" if dex_price > cex_price else "CEX->DEX"

    # threshold realistico per Base micro-arb
    if abs(spread) < 0.2:
        return None

    if abs(spread) > 20:
        return None

    return {
        "symbol": symbol,
        "spread": spread,
        "cex": cex_price,
        "dex": dex_price,
        "direction": direction
    }
