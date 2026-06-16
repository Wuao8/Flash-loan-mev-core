from scanner.profit_simulator import compute_net_profit


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
            enriched = compute_net_profit(op)

            if enriched["net_profit"] > 0:
                opportunities.append(enriched)
                print("PROFIT OPPORTUNITY:", enriched)

    return sorted(opportunities, key=lambda x: x["net_profit"], reverse=True)
