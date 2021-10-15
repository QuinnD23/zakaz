from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

AdminMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить сотрудника✅"),
        ],
        [
            KeyboardButton(text="Удалить сотрудника❌"),
        ],
        [
            KeyboardButton(text="Создать уведомление⚡"),
        ],
        [
            KeyboardButton(text="Редактировать уведомление✏"),
        ],
    ],
    resize_keyboard=True
)
EditMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Текст"),
        ],
        [
            KeyboardButton(text="Дата"),
        ],
        [
            KeyboardButton(text="Время"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
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
