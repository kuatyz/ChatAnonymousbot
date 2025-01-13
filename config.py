from dotenv import load_dotenv
import os
import logging

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7214861011:AAFE0oHuQMPoHgnnq1KInGLKiEALwyLzJhY")
ADMINS = os.environ.get("ADMIN", "1475365115")
DB_NAME = os.environ.get("DATABASE_NAME", "chatbot")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d"
)
logger = logging.getLogger("Bot")
