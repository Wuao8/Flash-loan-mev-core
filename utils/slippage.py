def estimate_slippage(spread_percent):
    """
    modello semplice: più spread = più slippage reale possibile
    """
    if spread_percent < 2:
        return 0.6
    if spread_percent < 5:
        return 1.2
    if spread_percent < 10:
        return 2.5
    return 4.0
