from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Main Menu
btn_with = KeyboardButton("Слова с аккордами")
btn_without = KeyboardButton("Без аккордов")
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_with, btn_without)

# Main Menu - button
btn_back = KeyboardButton("Главное меню")

# back chords Menu
back_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_back)