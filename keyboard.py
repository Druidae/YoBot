from telebot import types

# TODO: Think about this
# command_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
# start_kommand = types.KeyboardButton('/start')
# help_command = types.KeyboardButton('/help')
# language_selection_command = types.KeyboardButton('/language')
# command_keyboard.add(start_kommand, help_command, language_selection_command)


# Define a keyboard markup for language selection
language_keyboard = types.ReplyKeyboardMarkup(
    # row_width=2,  # Set the row width to 2, meaning two buttons appear in each row
    one_time_keyboard=True,  # Keyboard appears only once for the user
    resize_keyboard=True  # Allow the keyboard to be resized
)

# Create buttons for selecting Russian and English languages
russian_kommand = types.KeyboardButton('Russian')
english_command = types.KeyboardButton('English')

# Add the language buttons to the keyboard
language_keyboard.add(russian_kommand, english_command)
