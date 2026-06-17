print("FLASH LOAN SIGNAL BOT START (CLEAN MODE)")

from telegram_notifier import send_telegram
from scanner.scanner_engine import scan_market
from executor.engine import evaluate_opportunities


TRADE_SIZE = 10  # USD simulated


def main():

    ops = scan_market()
    executable = evaluate_opportunities(ops)

    if not executable:
        print("NO SIGNALS")
        return

    msg = "⚡ ARBITRAGE SIGNALS (SIMULATED DEMO MODE)\n\n"

    for i, op in enumerate(executable[:5], 1):

        profit_usd = op["true_net_profit"]
        roi_percent = (profit_usd / TRADE_SIZE) * 100

        msg += (
            f"{i}. {op['symbol']}\n"
            f"ROI: {roi_percent:.2f}%\n"
            f"Estimated Profit: ${profit_usd:.2f}\n"
            f"Spread: {op['spread']:.2f}%\n"
            f"Trade Size: ${TRADE_SIZE}\n\n"
        )

    send_telegram(msg)
    print(msg)


if __name__ == "__main__":
    main()
