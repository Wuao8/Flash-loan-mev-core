print("FLASH LOAN EXECUTION LAYER START")

from telegram_notifier import send_telegram
from scanner.scanner_engine import scan_market
from executor.engine import evaluate_opportunities


def main():

    ops = scan_market()

    executable = evaluate_opportunities(ops)

    if not executable:
        send_telegram("NO EXECUTABLE TRADES FOUND")
        print("NO EXECUTION")
        return

    msg = "⚡ EXECUTION READY OPPORTUNITIES\n\n"

    for i, op in enumerate(executable[:5], 1):
        msg += (
            f"{i}. {op['symbol']}\n"
            f"Net Profit: ${op['net_profit']:.2f}\n"
            f"Spread: {op['spread']:.2f}%\n"
            f"READY FOR EXECUTION\n\n"
        )

    send_telegram(msg)
    print(msg)


if __name__ == "__main__":
    main()
