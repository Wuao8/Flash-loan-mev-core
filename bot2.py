print("FLASH LOAN PROFIT SCANNER START")

from telegram_notifier import send_telegram
from scanner.scanner_engine import scan_market


def main():

    ops = scan_market()

    if not ops:
        send_telegram("NO PROFITABLE OPPORTUNITIES")
        print("NO PROFIT")
        return

    msg = "🚀 BASE PROFIT SCANNER\n\n"

    for i, op in enumerate(ops[:5], 1):
        msg += (
            f"{i}. {op['symbol']}\n"
            f"Net Profit: ${op['net_profit']:.2f}\n"
            f"Spread: {op['spread']:.2f}%\n"
            f"Gas: ${op['gas_cost']:.2f}\n\n"
        )

    send_telegram(msg)
    print(msg)


if __name__ == "__main__":
    main()
