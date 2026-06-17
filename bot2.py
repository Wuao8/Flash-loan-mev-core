print("FLASH LOAN EXECUTION LAYER START (DEMO SILENT MODE)")

from telegram_notifier import send_telegram
from scanner.scanner_engine import scan_market
from executor.engine import evaluate_opportunities


def main():

    ops = scan_market()
    executable = evaluate_opportunities(ops)

    # SILENT MODE: niente messaggi se non ci sono opportunità
    if not executable:
        print("NO OPPORTUNITIES (SILENT MODE)")
        return

    msg = "⚡ FLASH LOAN EXECUTION REPORT (SIMULATED)\n\n"

    total_profit = 0

    for i, op in enumerate(executable[:5], 1):

        profit = op["true_net_profit"]
        total_profit += profit

        msg += (
            f"{i}. {op['symbol']}\n"
            f"EXECUTED (SIMULATED)\n"
            f"Gross Profit: ${op['net_profit']:.2f}\n"
            f"Net Profit: ${profit:.2f}\n"
            f"Spread: {op['spread']:.2f}%\n\n"
        )

    msg += f"TOTAL SIMULATED PROFIT: ${total_profit:.2f}"

    send_telegram(msg)
    print(msg)


if __name__ == "__main__":
    main()
