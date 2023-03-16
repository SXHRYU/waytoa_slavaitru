from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# Problem Keyboard.
# problem_tag_button = KeyboardButton("Выберите тему.")
# problem_difficulty_button = KeyboardButton("Выберите сложность.")
# problem_problem_button = KeyboardButton("Выберите задачу.")

# problem_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# problem_kb.add(problem_button_choose)

# Navigation Keyboard.
navigation_button_cancel = KeyboardButton("Отменить")

navigation_kb = ReplyKeyboardMarkup(resize_keyboard=True)
navigation_kb.add(navigation_button_cancel)

# Menu Keyboard.
menu_problem_button = KeyboardButton("Выбрать задачу")
menu_help_button = KeyboardButton("Помощь")

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.row(menu_problem_button).row(menu_help_button)
