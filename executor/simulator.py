FLASH_LOAN_FEE_RATE = 0.0009
MIN_PROFIT_THRESHOLD = 0.05  # USD


def simulate_execution(opportunity):

    gross_profit = opportunity.get("gross_profit") or opportunity.get("net_profit", 0)

    if gross_profit <= 0:
        return {
            "valid": False,
            "true_profit": 0,
            "gas_cost": 0,
            "flash_fee": 0
        }

    flash_fee = gross_profit * FLASH_LOAN_FEE_RATE

    # gas realistico Base (micro swaps)
    gas_cost = 0.01

    true_profit = gross_profit - flash_fee - gas_cost

    if true_profit < MIN_PROFIT_THRESHOLD:
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
