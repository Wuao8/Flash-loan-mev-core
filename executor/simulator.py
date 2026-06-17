BASE_GAS_COST = 0.002  # ETH equivalente stimato su Base (demo)
FLASH_LOAN_FEE_RATE = 0.0009  # 0.09% tipico Aave-like
MIN_PROFIT_THRESHOLD = 0.5  # USD


def simulate_execution(opportunity):

    gross_profit = opportunity["net_profit"]

    # flash loan fee
    flash_fee = gross_profit * FLASH_LOAN_FEE_RATE

    # gas cost (fixed demo model)
    gas_cost = BASE_GAS_COST * 3000  # approx tx complexity scaling

    true_profit = gross_profit - flash_fee - gas_cost

    # validity checks
    if true_profit < MIN_PROFIT_THRESHOLD:
        return {
            "valid": False,
            "true_profit": true_profit,
            "gas_cost": gas_cost,
            "flash_fee": flash_fee
        }

    if opportunity["spread"] < 0.3:
        return {
            "valid": False,
            "true_profit": true_profit,
            "gas_cost": gas_cost,
            "flash_fee": flash_fee
        }

    return {
        "valid": True,
        "true_profit": true_profit,
        "gas_cost": gas_cost,
        "flash_fee": flash_fee
    }
