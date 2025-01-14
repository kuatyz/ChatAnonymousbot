from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import db
from config import *

api_id = API_ID
api_hash = API_HASH
access_token = BOT_TOKEN
user_state = {}

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=access_token)