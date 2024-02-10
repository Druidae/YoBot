from get_audio_from_youtube import get_audio
from dotenv import load_dotenv

from keyboard import command_keyboard

import telebot
import os

load_dotenv()

bot = telebot.TeleBot(token=os.environ['API_KEY'])


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello, send me video URL", reply_markup=command_keyboard)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Here is the Help part")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id, 'Your audio downloading now, please wait...')
    try:
        audio = get_audio(message.text)
        bot.send_audio(message.chat.id, audio)
    except Exception as ex:
        print(ex)
        bot.send_message(message.chat.id,
                         "Error while downloading video, check the URL or inform us about the error")


def main():
    try:
        bot.polling(none_stop=True, interval=0, timeout=60)
    finally:
        bot.stop_bot()


if __name__ == '__main__':
    main()