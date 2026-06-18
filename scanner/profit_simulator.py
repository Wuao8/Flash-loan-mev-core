FLASH_LOAN_FEE_RATE = 0.0009
BASE_GAS_COST = 0.01  # USD per tx (Base realistic micro swap)
SLIPPAGE_RATE = 0.003  # 0.3% base assumption
MIN_LIQUIDITY_USD = 5000


def compute_net_profit(opportunity, trade_size_usd=10):

    # safety
    if not opportunity:
        return {"net_profit": 0, "valid": False}

    buy_price = opportunity.get("buy_price")
    sell_price = opportunity.get("sell_price")

    if not buy_price or not sell_price:
        return {"net_profit": 0, "valid": False}

    # gross spread profit on trade size
    price_diff = sell_price - buy_price
    gross_profit = (price_diff / buy_price) * trade_size_usd

    # slippage cost (entry + exit)
    slippage_cost = trade_size_usd * SLIPPAGE_RATE * 2

    # flash loan fee
    flash_fee = gross_profit * FLASH_LOAN_FEE_RATE

    # gas
    gas_cost = BASE_GAS_COST

    net_profit = gross_profit - slippage_cost - flash_fee - gas_cost

    # liquidity sanity check (if available in op)
    buy_liq = opportunity.get("buy_liquidity", 1e9)
    sell_liq = opportunity.get("sell_liquidity", 1e9)

    if min(buy_liq, sell_liq) < MIN_LIQUIDITY_USD:
        return {
            "net_profit": net_profit,
            "valid": False,
            "reason": "low_liquidity"
        }

    # validity threshold
    if net_profit <= 0.02:
        return {
            "net_profit": net_profit,
            "valid": False
        }

    return {
        "net_profit": net_profit,
        "valid": True,
        "breakdown": {
            "gross_profit": gross_profit,
            "slippage": slippage_cost,
            "flash_fee": flash_fee,
            "gas": gas_cost
        }
    }
