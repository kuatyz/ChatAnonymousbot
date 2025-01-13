import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from database import *
from enum import Enum

access_token = BOT_TOKEN
bot = telebot.TeleBot(access_token)

# CLASS
class ParseMode(Enum):
    MARKDOWN = "Markdown"
    HTML = "HTML"

# MAIN MENU/SEMUA DEF
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    item1 = KeyboardButton('👥 Cari teman ngobrol')
    markup.add(item1)
    return markup

def process_age(message, gender):
    user_id = message.chat.id
    try:
        bot.send_message(user_id, 'Masukkan umur Anda:')
        age = int(message.text)
        bot.register_next_step_handler(message, process_name, gender, age)
    except ValueError:
        bot.send_message(user_id, '❌ Mohon masukkan umur yang valid.')
        bot.register_next_step_handler(message, process_age, gender)

def process_name(message, gender, age):
    user_id = message.chat.id

    first_name = message.from_user.first_name
    last_name = message.from_user.last_name if message.from_user.last_name else ''
    username = message.from_user.username if message.from_user.username else ''

    full_name = f"{first_name} {last_name}".strip() or username

    if db.add_user(user_id, full_name, age, gender):
        bot.send_message(
            user_id,
            f"✅ Data Anda telah berhasil ditambahkan!\n\n"
            f"🆔 **User ID**: `{user_id}`\n"
            f"👤 **Nama**: {full_name}\n"
            f"👫 **Jenis Kelamin**: {gender}\n"
            f"🎂 **Umur**: {age} Tahun",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu()
        )
    else:
        bot.send_message(user_id, '❌ Data Anda sudah ada di database.')

def stop_dialog():
    markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    item1 = KeyboardButton('🗣 Ceritakan profilmu padaku')
    item2 = KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup

def stop_search():
    markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    item1 = KeyboardButton('❌ Hentikan Pencarian')
    markup.add(item1)
    return markup

# START PERTAMA/WELCOME
@bot.message_handler(commands = ['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    item1 = KeyboardButton('Pria 👨')
    item2 = KeyboardButton('Wanita 👩‍🦱')
    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Hello, {0.first_name}! Selamat datang di bot anon. silahkan pilih jenis kelamin anda.'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = KeyboardButton('👥 Cari teman ngobrol')
    markup.add(item1)

    bot.send_message(message.chat.id, '📝 Меnu'.format(message.from_user), reply_markup = markup)

#HANDLER BOT ANON
@bot.message_handler(content_types = ['text'])
def bot_message(message):
    user_id = message.chat.id
    #PILIHAN GENDER
    if message.chat.type == 'private':
        if message.text == 'Pria 👨':
            if db.add_user(user_id, 'male'):
                bot.send_message(user_id, '✅ Jenis kelamin Anda telah berhasil ditambahkan!', reply_markup = main_menu())
                bot.send_message(user_id, 'Masukkan umur Anda:')
                bot.register_next_step_handler(message, process_age, 'male')
            else:
                bot.send_message(user_id, '❌ Data Anda sudah berada di database')
        
        elif message.text == 'Wanita 👩‍🦱':
            if db.add_user(user_id, 'female'):
                bot.send_message(user_id, '✅ Jenis kelamin Anda telah berhasil ditambahkan!', reply_markup = main_menu())
                bot.send_message(user_id, 'Masukkan umur Anda:')
                bot.register_next_step_handler(message, process_age, 'female')
            else:
                bot.send_message(user_id, '❌ Data Anda sudah berada di database')
        
        elif message.text == '👥 Cari teman ngobrol' or message.text == '✏️ Next dialogue':
            markup = ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = KeyboardButton('🔎 Boy')
            item2 = KeyboardButton('🔎 Girl')
            item3 = KeyboardButton('👩‍👨 Random')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Siapa yang harus dicari?', reply_markup = markup)

        elif message.text == '❌ Hentikan Pencarian':
            db.remove_from_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌ Pencarian dihentikan, tulis /menu', reply_markup = main_menu())
        
        elif message.text == '🔎 Boy':
            user_info = db.get_all_users('male')
            chat_two = user_info[0]
            if db.add_chat(message.chat.id, chat_two) == False:
                db.add_to_queue(message.chat.id, db.get_all_users(message.chat.id))
                bot.send_message(message.chat.id, '👻 Cari teman bicara', reply_markup = stop_search())
            else:
                mess = 'Teman bicara telah ditemukan! Untuk menghentikan dialog, ketik /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        
        elif message.text == '🔎 Girl':
            user_info = db.get_all_users('female')
            chat_two = user_info[0]
            if db.add_chat(message.chat.id, chat_two) == False:
                db.add_to_queue(message.chat.id, db.get_all_users(message.chat.id))
                bot.send_message(message.chat.id, '👻 Cari teman bicara', reply_markup = stop_search())
            else:
                mess = 'Teman bicara telah ditemukan! Untuk menghentikan dialog, ketik /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        elif message.text == '👩‍👨 Acak':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.add_chat(message.chat.id, chat_two) == False:
                db.add_to_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Cari teman bicara', reply_markup = stop_search())
            else:
                mess = 'Teman bicara telah ditemukan! Untuk menghentikan dialog, ketik /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        elif message.text == '🗣 Ceritakan profilmu padaku':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info != False:
                if message.from_user.username:
                    bot.send_message(chat_info[1], '@' + message.from_user.username)
                    bot.send_message(message.chat.id, '🗣 Ceritakan profilmu padaku')
                else:
                    bot.send_message(message.chat.id, '❌ Akun Anda tidak memiliki nama pengguna yang ditentukan')
            else:
                bot.send_message(message.chat.id, '❌ Anda belum memulai dialog!')
        
        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            else:
                bot.send_message(message.chat.id, '❌ Anda belum memulai dialog!')


@bot.message_handler(content_types='stickers')
def bot_stickers(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Anda belum memulai dialog!')

@bot.message_handler(content_types='voice')
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_voice(chat_info[1], message.voice.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Anda belum memulai dialog!')