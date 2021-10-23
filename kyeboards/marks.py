from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

StartMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Новый заказ🛠"),
        ],
        [
            KeyboardButton(text="Мои заказы📚"),
        ],
        [
            KeyboardButton(text="Информация📖"),
        ],
    ],
    resize_keyboard=True
)

StartLimitMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Мои заказы📚"),
        ],
        [
            KeyboardButton(text="Информация📖"),
        ],
    ],
    resize_keyboard=True
)

MyOrdersMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подтвердить✅"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

AdminMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ответить💥"),
        ],
    ],
    resize_keyboard=True
)

BackMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

AcceptMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да✅"),
        ],
        [
            KeyboardButton(text="Нет❌"),
        ],
    ],
    resize_keyboard=True
)

AnswerMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Заказать🔥"),
        ],
        [
            KeyboardButton(text="Позже🕐"),
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

