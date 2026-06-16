from utils.gas_estimator import estimate_base_gas_cost
from utils.slippage import estimate_slippage


def compute_net_profit(opportunity):
    spread = opportunity["spread"]

    notional = 1000  # simuliamo 1000$ trade size

    gross_profit = notional * (spread / 100)

    slippage_pct = estimate_slippage(spread)
    slippage_cost = notional * (slippage_pct / 100)

    gas_cost = estimate_base_gas_cost()

    net_profit = gross_profit - slippage_cost - gas_cost

    return {
        **opportunity,
        "gross_profit": gross_profit,
        "slippage_cost": slippage_cost,
        "gas_cost": gas_cost,
        "net_profit": net_profit
    }
