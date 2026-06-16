from scanner.token_list import get_tokens
from scanner.dex_prices import get_base_dex_price
from scanner.arbitrage import find_opportunity


# MOCK CEX (per ora, poi lo colleghiamo davvero)
def get_mock_cex_price(symbol):
    return 1.0


def scan_market():
    tokens = get_tokens()

    opportunities = []

    print(f"SCANNING {len(tokens)} TOKENS ON BASE...")

    for symbol, address in tokens.items():

        dex_price = get_base_dex_price(address)
        cex_price = get_mock_cex_price(symbol)

        if not dex_price:
            continue

        op = find_opportunity(symbol, cex_price, dex_price)

        if op:
            opportunities.append(op)
            print("OPPORTUNITY:", op)

    return sorted(opportunities, key=lambda x: x["spread"], reverse=True)
