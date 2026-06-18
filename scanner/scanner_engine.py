from scanner.token_list import get_tokens
from scanner.dex_prices import get_token_prices_multi_dex
from scanner.arbitrage import find_opportunity
from scanner.profit_simulator import compute_net_profit


def scan_market():

    tokens = get_tokens()
    opportunities = []

    print(f"SCANNING {len(tokens)} TOKENS ON BASE...")

    for symbol, address in tokens.items():

        # 1. multi-DEX prices
        dex_prices = get_token_prices_multi_dex(address)

        # 2. find arbitrage opportunity (cross DEX)
        op = find_opportunity(symbol, None, dex_prices)

       if not op:
           continue

       op["spread"] = op.get("spread", 0)

       enriched = compute_net_profit(op)

    # sort by profit
    opportunities.sort(key=lambda x: x["net_profit"], reverse=True)

    print(f"VALID OPPORTUNITIES: {len(opportunities)}")

    return opportunities
