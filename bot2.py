print("FLASH LOAN EXECUTION LAYER START (DEMO MODE)")

from telegram_notifier import send_telegram
from scanner.scanner_engine import scan_market
from executor.engine import evaluate_opportunities


def main():

    ops = scan_market()
    executable = evaluate_opportunities(ops)

    if not executable:
        send_telegram("NO REAL EXECUTABLE ARB OPPORTUNITIES FOUND (AFTER SIMULATION)")
        print("NO EXECUTION")
        return

    msg = "⚡ REALISTIC FLASH LOAN OPPORTUNITIES (DEMO MODE)\n\n"

    for i, op in enumerate(executable[:5], 1):

        msg += (
            f"{i}. {op['symbol']}\n"
            f"True Net Profit: ${op['true_net_profit']:.2f}\n"
            f"Gross Profit: ${op['net_profit']:.2f}\n"
            f"Spread: {op['spread']:.2f}%\n"
            f"Gas Est: {op['estimated_gas']:.4f}\n"
            f"Flash Fee: {op['estimated_flash_fee']:.4f}\n"
            f"STATUS: SIMULATED EXECUTION OK\n\n"
        )

    send_telegram(msg)
    print(msg)


if __name__ == "__main__":
    main()
