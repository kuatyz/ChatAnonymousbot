from dotenv import load_dotenv
import os
from logging import basicConfig, INFO, WARNING, getLogger, Logger

load_dotenv()

API_ID = os.environ.get("API_ID","")
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMINS = os.environ.get("ADMIN", "")
DB_NAME = os.environ.get("DATABASE_NAME", "")

basicConfig(level=INFO, format="[%(levelname)s] - %(message)s")
getLogger("pyrogram").setLevel(WARNING)
def LOGGER(name: str) -> Logger:
    return getLogger(name)