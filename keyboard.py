from telebot import types


command_keyboard = types.ReplyKeyboardMarkup(row_width=2)
start_kommand = types.KeyboardButton('/start')
help_command = types.KeyboardButton('/help')
command_keyboard.add(start_kommand, help_command)
