def estimate_base_gas_cost():
    """
    stima MOLTO conservativa su Base L2
    """
    gas_price_gwei = 0.05  # base è cheap
    gas_limit = 350000     # swap + routing + checks

    eth_price_usd = 3000   # fallback statico

    gas_cost_eth = (gas_price_gwei * gas_limit) / 1e9
    gas_cost_usd = gas_cost_eth * eth_price_usd

    return gas_cost_usd
