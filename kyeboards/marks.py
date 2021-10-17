from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

StartMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Новый заказ🛠"),
        ],
    ],
    resize_keyboard=True
)
ChoiceAutoMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить авто➕"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

ChoicePlaceMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить район➕"),
        ],
    ],
    resize_keyboard=True
)

BonusMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Нет скидки❌"),
        ],
    ],
    resize_keyboard=True
)

