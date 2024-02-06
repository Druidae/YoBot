from get_audio_from_youtube import get_audio
from dotenv import load_dotenv

import telebot
import os

load_dotenv()

bot = telebot.TeleBot(token=os.environ['API_KEY'])


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    # audio = open(f'data/{get_audio(message.text)}.mp3', 'rb')
    audio = get_audio(message.text)
    bot.send_audio(message.chat.id, audio)


def main():
    try:
        bot.infinity_polling()
    finally:
        bot.stop_bot()


if __name__ == '__main__':
    main()