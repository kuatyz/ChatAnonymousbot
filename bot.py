import telebot
from telebot.types import *
from config import BOT_TOKEN
from database import db

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id

    user_data = db.get_user(user_id)
    if user_data:
        bot.send_message(
            message.chat.id,
            f"Selamat datang kembali, {user_data[2]}!\nSilahkan ketik /search untuk mecari pasangan")
    else:
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn_pria = KeyboardButton("Pria")
        btn_wanita = KeyboardButton("Wanita")
        markup.add(btn_pria, btn_wanita)
        bot.send_message(message.chat.id, "Pilih jenis kelamin Anda:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_gender(message):
    gender = message.text.strip()
    if gender == 'Pria' or gender == 'Wanita':
        bot.send_message(message.chat.id, f"Anda memilih {gender}.")
        bot.register_next_step_handler(message, ask_age, gender)
    else:
        bot.send_message(message.chat.id, "Tolong pilih 'Pria' atau 'Wanita'.")

@bot.message_handler(func=lambda message: message.text == "Kembali")
def go_back_to_gender(message):
    bot.send_message(message.chat.id, "Tolong pilih 'Pria' atau 'Wanita'.")
    send_welcome(message)

def ask_age(message, gender):
    bot.send_message(message.chat.id, "Berapa usia Anda?")
    bot.register_next_step_handler(message, save_user_data, gender)

def save_user_data(message, gender):
    try:
        age = int(message.text)
        chat_id = message.chat.id
        user_id = message.from_user.id
        name = message.from_user.first_name
        db.set_gender(user_id, chat_id, name, gender, age)

        bot.send_message(
            message.chat.id,
            f"Data Anda telah disimpan!\n"
            f"User ID: {user_id}\n"
            f"Nama: {name}\n"
            f"Gender: {gender}\n"
            f"Age: {age}"
        )
    except ValueError:
        bot.send_message(message.chat.id, "Usia tidak valid, coba lagi.")
        bot.register_next_step_handler(message, save_user_data, gender)
