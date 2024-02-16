from telebot import types

# TODO: Think about this
# command_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
# start_kommand = types.KeyboardButton('/start')
# help_command = types.KeyboardButton('/help')
# language_selection_command = types.KeyboardButton('/language')
# command_keyboard.add(start_kommand, help_command, language_selection_command)


language_keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
russian_kommand = types.KeyboardButton('Russian')
english_command = types.KeyboardButton('English')
language_keyboard.add(russian_kommand, english_command)
