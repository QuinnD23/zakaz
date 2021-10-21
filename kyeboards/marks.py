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
            KeyboardButton(text="Создать уведомление⚡️"),
        ],
        [
            KeyboardButton(text="Редактировать уведомление✏️"),
        ],
    ],
    resize_keyboard=True
)
EditDayMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Текст✏️"),
        ],
        [
            KeyboardButton(text="Дата🗓"),
        ],
        [
            KeyboardButton(text="Время🕐"),
        ],
        [
            KeyboardButton(text="Cотрудники👨"),
        ],
        [
            KeyboardButton(text="Удалить❌"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

AddRemoveMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить✅"),
        ],
        [
            KeyboardButton(text="Удалить❌"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

EditWeekMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Текст✏️"),
        ],
        [
            KeyboardButton(text="День недели☀️"),
        ],
        [
            KeyboardButton(text="Время🕐"),
        ],
        [
            KeyboardButton(text="Удалить❌"),
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

NotifyMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="День недели☀️"),
        ],
        [
            KeyboardButton(text="Конкретная дата🌩"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)
MembersMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Стоп⛔️"),
        ],
    ],
    resize_keyboard=True
)
