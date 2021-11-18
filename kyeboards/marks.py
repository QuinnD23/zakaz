from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главный администратор
MainAdminMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Администраторы💫"),
        ],
        [
            KeyboardButton(text="Сотрудники👩‍💼"),
        ],
        [
            KeyboardButton(text="Интерфейс Пользователя📱"),
        ],
        [
            KeyboardButton(text="Услуги📙"),
        ],
    ],
    resize_keyboard=True
)

EditAdminsMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить Администратора💫"),
        ],
        [
            KeyboardButton(text="Удалить Администратора❌"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

EditWorkersMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить Сотрудника👩‍💼"),
        ],
        [
            KeyboardButton(text="Удалить Сотрудника❌"),
        ],
        [
            KeyboardButton(text="Редактировать Услуги📙"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

EditServicesMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить Услугу📙"),
        ],
        [
            KeyboardButton(text="Удалить Услугу❌"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

EditFaceMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Приветствие🤚"),
        ],
        [
            KeyboardButton(text="Рабочее Время⌚️"),
        ],
        [
            KeyboardButton(text="Завершение☑️"),
        ],
        [
            KeyboardButton(text="Контакты📚"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

EditContactsMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить Контакт📚"),
        ],
        [
            KeyboardButton(text="Удалить Контакт❌"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

# Обычный Администратор
AdminMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Сотрудники👩‍💼"),
        ],
        [
            KeyboardButton(text="Интерфейс Пользователя📱"),
        ],
        [
            KeyboardButton(text="Услуги📙"),
        ],
    ],
    resize_keyboard=True
)

# Пользователь

UserMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Записаться🔹"),
        ],
        [
            KeyboardButton(text="Мои контакты📱"),
        ]
    ],
    resize_keyboard=True
)

EditUsersContactsMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Изменить Контакт📘"),
        ],
        [
            KeyboardButton(text="Назад◀️"),
        ]
    ],
    resize_keyboard=True
)

# Общее
BackMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

StopMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Стоп⛔️"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)
