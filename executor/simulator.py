def simulate_execution(opportunity):

    """
    qui simuliamo se la trade sarebbe eseguibile
    (senza ancora smart contract flash loan)
    """

    if opportunity["net_profit"] < 1:
        return False

    if opportunity["spread"] < 1:
        return False

    return True
