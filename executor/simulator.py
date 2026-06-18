FLASH_LOAN_FEE_RATE = 0.0009
MIN_PROFIT_THRESHOLD = 0.05  # molto più realistico per demo


def simulate_execution(opportunity):

    gross_profit = opportunity["net_profit"]

    # flash loan fee realistico
    flash_fee = gross_profit * FLASH_LOAN_FEE_RATE

    # gas realistico su Base (range piccolo, non fisso enorme)
    gas_cost = 0.01  # USD stimato per swap semplice

    true_profit = gross_profit - flash_fee - gas_cost

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
