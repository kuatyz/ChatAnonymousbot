from dotenv import load_dotenv
import os
import logging

load_dotenv()

API_ID = os.environ.get("API_ID","")
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMINS = os.environ.get("ADMIN", "")
DB_NAME = os.environ.get("DATABASE_NAME", "")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d"
)
logger = logging.getLogger("Bot")
