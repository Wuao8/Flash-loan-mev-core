print("FLASH LOAN BOT V1 START")

from telegram_notifier import send_telegram


def main():
    send_telegram("🚀 Bot avviato correttamente (TEST MODE)")
    print("BOT ONLINE")


if __name__ == "__main__":
    main()
