from get_audio_from_youtube import get_audio
from dotenv import load_dotenv

from keyboard import language_keyboard, command_keyboard
from languages import sentence

import telebot
import os

load_dotenv()

bot = telebot.TeleBot(token=os.environ['API_KEY'])
language = 'english'


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global language
    bot.send_message(message.chat.id,
                     "Hello, I'm YoBot\nPlease choose prefer language\n default language - English",
                     reply_markup=language_keyboard)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, sentence[language]['help'])


@bot.message_handler(func=lambda message: message.text == 'russian' or message.text == 'english')
def set_language(message):
    global language
    language = message.text
    bot.send_message(message.chat.id, f"Chosen language is: {language}")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    print(message.text)
    bot.send_message(message.chat.id, sentence[language]['start_download'])
    try:
        audio = get_audio(message.text)
        bot.send_audio(message.chat.id, audio)
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
