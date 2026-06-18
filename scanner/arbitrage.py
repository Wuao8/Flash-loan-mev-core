def find_opportunity(symbol, cex_price, dex_prices):
    """
    dex_prices = lista da multi-DEX engine
    """

    if not dex_prices or len(dex_prices) < 2:
        return None

    # ordina per prezzo
    sorted_by_price = sorted(dex_prices, key=lambda x: x["price"])

    low = sorted_by_price[0]
    high = sorted_by_price[-1]

    low_price = low["price"]
    high_price = high["price"]

    if low_price <= 0:
        return None

    spread = ((high_price - low_price) / low_price) * 100

    if spread < 0.2:   # micro inefficiency threshold Base
        return None

    if spread > 20:
        return None

    direction = "BUY_LOW_SELL_HIGH"

    gross_profit = high_price - low_price

    return {
        "symbol": symbol,
        "spread": spread,
        "gross_profit": gross_profit,
        "buy_dex": low.get("dex"),
        "sell_dex": high.get("dex"),
        "buy_price": low_price,
        "sell_price": high_price,
        "direction": direction
    }
