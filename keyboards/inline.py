from aiogram import types


def create_kb(text, data):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text, callback_data=data)

    keyboard.add(button)
    return keyboard


def create_kb_multi(buttons):
    keyboard = types.InlineKeyboardMarkup()
    for text, data in buttons:
        button = types.InlineKeyboardButton(text, callback_data=data)
        keyboard.add(button)

    return keyboard
