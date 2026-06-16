def find_opportunity(symbol, cex_price, dex_price):

    if not cex_price or not dex_price:
        return None

    spread = abs((cex_price - dex_price) / cex_price) * 100

    if spread < 1.0:
        return None

    if spread > 25:
        return None

    direction = "DEX->CEX" if dex_price < cex_price else "CEX->DEX"

    return {
        "symbol": symbol,
        "spread": spread,
        "cex": cex_price,
        "dex": dex_price,
        "direction": direction
    }
