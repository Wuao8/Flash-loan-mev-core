from executor.simulator import simulate_execution


def evaluate_opportunities(opportunities):
    executable = []

    if not opportunities:
        return []

    for op in opportunities:

        result = simulate_execution(op)

        if not result or not result.get("valid"):
            continue

        true_profit = result.get("true_profit", 0)

        # filtro minimo realistico (evita micro noise)
        if true_profit <= 0:
            continue

        op["estimated_gas"] = result.get("gas_cost", 0)
        op["estimated_flash_fee"] = result.get("flash_fee", 0)
        op["true_net_profit"] = true_profit

        executable.append(op)

    return sorted(executable, key=lambda x: x["true_net_profit"], reverse=True)
