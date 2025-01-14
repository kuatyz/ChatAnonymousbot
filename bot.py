from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import db
from config import *

api_id = API_ID
api_hash = API_HASH
access_token = BOT_TOKEN
user_state = {}

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=access_token)

# START
@bot.on_message(filters.command('start'))
async def start(client, message):
    user = db.get_user(message.from_user.id)
    
    if user is None:
        inline_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Я Парень 👨", callback_data="male"),
                 InlineKeyboardButton("Я Девушка 👩‍🦱", callback_data="female")]
            ]
        )
        await message.reply(f"Hello, {message.from_user.first_name}! Selamat Datang di bot Anon!, Pilih gender kamu", reply_markup=inline_markup)
    else:
        await message.reply("Informasi kamu sudah berada di database, lanjutkan pencarian /search")

@bot.on_callback_query()
async def handle_callback(client, callback_query):
    user_id = callback_query.from_user.id
    gender_preference = callback_query.data
    name = callback_query.from_user.first_name
    gender = gender_preference

    db.add_queue(user_id, gender_preference)
    age_message = await client.ask(user_id, "Masukkan usia Anda (dalam tahun):")

    try:
        age = int(age_message.text)
        if age < 0 or age > 120:
            await age_message.reply("Harap masukkan usia yang valid.")
        else:
            db.add_user(user_id, name, gender, age)
            info_message = f"Informasi berhasil disimpan:\nNama: {name}\nUser ID: {user_id}\nGender: {gender}\nUmur: {age}"
            await age_message.reply(info_message)
    except ValueError:
        await age_message.reply("Harap masukkan angka usia yang valid.")