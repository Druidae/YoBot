from get_audio_async import get_audio, check_size
from keyboard import language_keyboard
from languages import sentence

from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from telebot import types

import asyncio
import os

# Load environment variables from .env file
load_dotenv()

# Default language setting
language = "English"

# Initialize TeleBot with API key from environment variable
bot = AsyncTeleBot(token=os.environ["API_KEY"])


# Handle '/start' command
@bot.message_handler(commands=["start"])
async def send_welcome(message):
    # Send welcome message on default language
    await bot.send_message(
        message.chat.id,
        "Hello, I'm YoBot :)\n You can send me link and I return you audio file\n If you want to "
        "change language, please use /language command.(default language - English)",
    )


# Handle '/help' command
@bot.message_handler(commands=["help"])
async def get_help(message):
    # Send help message based on selected language
    await bot.send_message(message.chat.id, sentence[language]["help"])


# Handle '/language' command to change language
@bot.message_handler(commands=["language"])
async def change_language(message):
    # Send message showing current language and provide language selection keyboard
    await bot.send_message(
        message.chat.id,
        f"Current language is: {language}",
        reply_markup=language_keyboard
    )


# Handle language selection
@bot.message_handler(func=lambda message: message.text in ("Russian", "English"))
async def set_language(message):
    global language
    # Update global language variable based on user's selection
    language = message.text
    await bot.send_message(message.chat.id, f"Chosen language is: {language}")


# Handle '/check' command to check link validity
@bot.message_handler(commands=["check_link"])
async def check_link(message):
    markup = types.ForceReply(selective=False)
    # Provide a force reply to allow users to input the link they want to check
    await bot.send_message(
        message.chat.id, sentence[language]["check_link"], reply_markup=markup
    )


# Handle text messages
@bot.message_handler(func=lambda message: True)
async def text_message(message):
    if (
        message.reply_to_message
        and message.reply_to_message.text == sentence[language]["check_link"]
    ):
        # Check audiofile size from provided link
        try:
            ret_code = await check_size(message.text)
            await bot.send_message(message.chat.id, sentence[language][ret_code])
        except Exception as ex:
            print(f"[!] {ex}")
            await bot.send_message(
                message.chat.id, sentence[language]["download_error"]
            )
    else:
        await bot.send_message(message.chat.id, sentence[language]["start_download"])
        # Download audiofile from the provided link
        try:
            audio_patch = await get_audio(message.text)

            if audio_patch != "This file is too big":
                # If audio obtained successfully, send it to the user
                await bot.send_audio(message.chat.id, open(audio_patch, "rb"))
                os.remove(audio_patch)
            else:
                await bot.send_message(
                    message.chat.id, sentence[language]["file_size_error"]
                )
        except Exception as ex:
            print(ex)
            await bot.send_message(
                message.chat.id, sentence[language]["download_error"]
            )


# Entry point of the program
def main():
    # Start polling for updates
    asyncio.run(bot.polling(none_stop=True, interval=0, timeout=40))


# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
