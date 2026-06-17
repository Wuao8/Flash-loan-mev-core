from executor.simulator import simulate_execution


def evaluate_opportunities(opportunities):
    executable = []

    for op in opportunities:

        # simulazione realistica
        result = simulate_execution(op)

        if result["valid"]:
            op["estimated_gas"] = result["gas_cost"]
            op["estimated_flash_fee"] = result["flash_fee"]
            op["true_net_profit"] = result["true_profit"]

            executable.append(op)

    return sorted(executable, key=lambda x: x["true_net_profit"], reverse=True)
