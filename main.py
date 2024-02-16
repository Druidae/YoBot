from get_audio_from_youtube import get_audio, get_info
from dotenv import load_dotenv
from telebot import types

from keyboard import language_keyboard
from languages import sentence

import telebot
import os

load_dotenv()

bot = telebot.TeleBot(token=os.environ['API_KEY'])
language = 'English'


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global language
    bot.send_message(message.chat.id,
                     "Hello, I'm YoBot :)\n You can send me link and I return you audio file\n If you want to change "
                     "language, please use /language command.(default language - English)")


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, sentence[language]['help'])


@bot.message_handler(commands=['language'])
def change_language(message):
    bot.send_message(message.chat.id, f"Current language is: {language}", reply_markup=language_keyboard)


@bot.message_handler(func=lambda message: message.text == 'Russian' or message.text == 'English')
def set_language(message):
    global language
    language = message.text
    bot.send_message(message.chat.id, f"Chosen language is: {language}")


@bot.message_handler(commands=['check_link'])
def check_link(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, sentence[language]["check_link"], reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def text_message(message):
    if message.reply_to_message and message.reply_to_message.text == sentence[language]['check_link']:
        try:
            bot.send_message(message.chat.id, sentence[language][get_info(message.text)])
        except Exception as ex:
            print(f"[!] {ex}")
            bot.send_message(message.chat.id, sentence[language]['download_error'])
    else:
        bot.send_message(message.chat.id, sentence[language]['start_download'])
        try:
            audio = get_audio(message.text)
            if audio != 'This file is too big':
                bot.send_audio(message.chat.id, audio)
            else:
                bot.send_message(message.chat.id, sentence[language]['file_size_error'])
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id,
                             sentence[language]['download_error'])


def main():
    try:
        bot.polling(none_stop=True, interval=0, timeout=60)
    finally:
        bot.stop_bot()


if __name__ == '__main__':
    main()
