from scanner.token_list import get_tokens
from scanner.dex_prices import get_base_dex_price
from scanner.arbitrage import find_opportunity
from scanner.profit_simulator import compute_net_profit


# MOCK CEX (temporaneo)
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

        if not op:
            continue

        enriched = compute_net_profit(op)

        # filtro finale: solo profitto reale positivo
        if enriched["net_profit"] > 0:

            opportunities.append(enriched)

            print(
                f"PROFIT OK {symbol} | "
                f"NET=${enriched['net_profit']:.2f} | "
                f"SPREAD={enriched['spread']:.2f}%"
            )

    # ordina per profitto netto
    opportunities.sort(key=lambda x: x["net_profit"], reverse=True)

    print(f"VALID OPPORTUNITIES: {len(opportunities)}")

    return opportunities
