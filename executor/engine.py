from executor.simulator import simulate_execution


def evaluate_opportunities(opportunities):

    executable = []

    for op in opportunities:

        if simulate_execution(op):
            executable.append(op)

    return executable
