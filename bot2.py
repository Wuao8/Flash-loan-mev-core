print("FLASH LOAN SCANNER START")

from telegram_notifier import send_telegram
from scanner.scanner_engine import scan_market


def main():

    ops = scan_market()

    if not ops:
        send_telegram("NO ARB OPPORTUNITIES (BASE SCANNER)")
        print("NO OPPORTUNITIES")
        return

    msg = "🚀 BASE SCANNER RESULTS\n\n"

    for i, op in enumerate(ops[:5], 1):
        msg += (
            f"{i}. {op['symbol']}\n"
            f"Spread: {op['spread']:.2f}%\n"
            f"Direction: {op['direction']}\n\n"
        )

    send_telegram(msg)
    print(msg)


if __name__ == "__main__":
    main()
