from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
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
        # Menggunakan KeyboardButton untuk memilih gender
        markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton("Я Парень 👨"), KeyboardButton("Я Девушка 👩‍🦱")]
            ],
            resize_keyboard=True
        )
        await message.reply(f"Hello, {message.from_user.first_name}! Selamat Datang di bot Anon!, Pilih gender kamu", reply_markup=markup)
    else:
        await message.reply("Informasi kamu sudah berada di database, lanjutkan pencarian /search")

@bot.on_message(filters.text)
async def handle_gender_choice(client, message):
    user_id = message.from_user.id
    gender = message.text.strip()
    name = message.from_user.first_name

    if gender in ["Я Парень 👨", "Я Девушка 👩‍🦱"]:
        await message.reply("Masukkan usia Anda (dalam tahun):")
        
        try:
            # Menunggu input usia
            age_response = await client.listen(message.chat.id)
            age = int(age_response.text)

            if age < 0 or age > 120:
                await age_response.reply("Harap masukkan usia yang valid.")
            else:
                # Menyimpan informasi pengguna
                db.add_user(user_id, name, gender, age)
                info_message = f"Informasi berhasil disimpan:\nNama: {name}\nUser ID: {user_id}\nGender: {gender}\nUmur: {age}"
                await age_response.reply(info_message)
        except ValueError:
            await age_response.reply("Harap masukkan angka usia yang valid.")
    else:
        # Jika pengguna mengirimkan pesan selain pilihan gender yang sah
        await message.reply("Pilih salah satu gender yang tersedia: Я Парень 👨 atau Я Девушка 👩‍🦱")