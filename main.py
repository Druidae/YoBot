#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   THIS IS OLD FILE, PLEASE USING bot.py
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from get_audio import get_audio, check_size
from keyboard import language_keyboard
from languages import sentence

from dotenv import load_dotenv
from telebot import types

import telebot
import os

# Load environment variables from .env file
load_dotenv()

# Default language setting
language = "English"


# Initialize TeleBot with API key from environment variable
bot = telebot.TeleBot(token=os.environ["API_KEY"])


# Handle '/start' command
@bot.message_handler(commands=["start"])
def send_welcome(message):
    # Send welcome message on default language
    bot.send_message(
        message.chat.id,
        "Hello, I'm YoBot :)\n You can send me link and I return you audio file\n If you want to change "
        "language, please use /language command.(default language - English)",
    )


# Handle '/help' command
@bot.message_handler(commands=["help"])
def get_help(message):
    # Send help message based on selected language
    bot.send_message(message.chat.id, sentence[language]["help"])


# Handle '/language' command to change language
@bot.message_handler(commands=["language"])
def change_language(message):
    # Send message showing current language and provide language selection keyboard
    bot.send_message(
        message.chat.id,
        f"Current language is: {language}",
        reply_markup=language_keyboard,
    )


# Handle language selection
@bot.message_handler(func=lambda message: message.text in ("Russian", "English"))
def set_language(message):
    global language
    # Update global language variable based on user's selection
    language = message.text
    bot.send_message(message.chat.id, f"Chosen language is: {language}")


# Handle '/check' command to check link validity
@bot.message_handler(commands=["check_link"])
def check_link(message):
    markup = types.ForceReply(selective=False)
    # Provide a force reply to allow users to input the link they want to check
    bot.send_message(
        message.chat.id, sentence[language]["check_link"], reply_markup=markup
    )


# Handle text messages
@bot.message_handler(func=lambda message: True)
def text_message(message):
    if (
        message.reply_to_message
        and message.reply_to_message.text == sentence[language]["check_link"]
    ):
        # Check audiofile size from provided link
        try:
            bot.send_message(
                message.chat.id, sentence[language][check_size(message.text)]
            )
        except Exception as ex:
            print(f"[!] {ex}")
            bot.send_message(message.chat.id, sentence[language]["download_error"])
    else:
        bot.send_message(message.chat.id, sentence[language]["start_download"])
        # Download audiofile from the provided link
        try:
            audio = get_audio(message.text)
            if audio != "This file is too big":
                # If audio obtained successfully, send it to the user
                bot.send_audio(message.chat.id, audio)
            else:
                bot.send_message(message.chat.id, sentence[language]["file_size_error"])
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, sentence[language]["download_error"])


# Entry point of the program
def main():
    try:
        # Start polling for updates
        bot.polling(none_stop=True, interval=0, timeout=60)
    finally:
        # Stop the bot if an exception occurs
        bot.stop_bot()


# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
