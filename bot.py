from get_audio_from_youtube_async import get_audio, get_info
from keyboard import language_keyboard
from languages import sentence

from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from telebot import types

import asyncio
import os

load_dotenv()

bot = AsyncTeleBot(token=os.environ['API_KEY'])
language = 'English'


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.send_message(message.chat.id,
                           "Hello, I'm YoBot :)\n You can send me link and I return you audio file\n If you want to "
                           "change language, please use /language command.(default language - English)")


@bot.message_handler(commands=['help'])
async def get_help(message):
    await bot.send_message(message.chat.id, sentence[language]['help'])


@bot.message_handler(commands=['language'])
async def change_language(message):
    await bot.send_message(message.chat.id, f"Current language is: {language}", reply_markup=language_keyboard)


@bot.message_handler(func=lambda message: message.text == 'Russian' or message.text == 'English')
async def set_language(message):
    global language
    language = await message.text
    await bot.send_message(message.chat.id, f"Chosen language is: {language}")


@bot.message_handler(commands=['check_link'])
async def check_link(message):
    markup = types.ForceReply(selective=False)
    await bot.send_message(message.chat.id, sentence[language]["check_link"], reply_markup=markup)


@bot.message_handler(func=lambda message: True)
async def text_message(message):
    if message.reply_to_message and message.reply_to_message.text == sentence[language]['check_link']:
        try:
            ret_code = await get_info(message.text)
            await bot.send_message(message.chat.id, sentence[language][ret_code])
        except Exception as ex:
            print(f"[!] {ex}")
            await bot.send_message(message.chat.id, sentence[language]['download_error'])
    else:
        await bot.send_message(message.chat.id, sentence[language]['start_download'])
        try:
            audio_patch = await get_audio(message.text)

            if audio_patch != 'This file is too big':
                await bot.send_audio(message.chat.id, open(audio_patch, 'rb'))
                os.remove(audio_patch)
            else:
                await bot.send_message(message.chat.id, sentence[language]['file_size_error'])
        except Exception as ex:
            print(ex)
            await bot.send_message(message.chat.id,
                                   sentence[language]['download_error'])


def main():
    asyncio.run(bot.polling(none_stop=True, interval=0, timeout=40))


if __name__ == '__main__':
    main()
