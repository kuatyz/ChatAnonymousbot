from dotenv import load_dotenv
import os
import logging

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMINS = os.environ.get("ADMIN", "")
DB_NAME = os.environ.get("DATABASE_NAME", "")

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] - %(message)s")
logging.getLogger("telebot").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

logger = LOGGER("INFO")
