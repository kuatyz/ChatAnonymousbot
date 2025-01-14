from config import LOGGER
from bot import bot

logger = LOGGER("Bot")

def log_bot_info():
    try:
        bot_info = bot.get_me()
        bot_name = bot_info.first_name
        bot_username = bot_info.username
        logger.info(
            f"Bot: {bot_name}\n"
            f"Username: @{bot_username}\n"
            f"🔥 Bot Telah Aktif 🔥"
        )
    except Exception as e:
        logger.warning(f"Gagal mengambil informasi bot: {e}")

def main():
    log_bot_info()
    try:
        bot.polling()
    except Exception as e:
        logger.warning(f"Gagal memulai bot: {e}")

if __name__ == "__main__":
    main()