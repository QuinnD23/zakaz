from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.filters import Command

# config
from data.config import code

# re
import re

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import AdminMenu


@dp.message_handler(state=StateMachine.NotifyText)
async def mess(message: Message):
    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----
    else:
        # ----- back
        if message.text == "Отменить◀️":
            await message.answer("Возвращаю...", reply_markup=AdminMenu)
            await StateMachine.Admin.set()
        # -----
        else:
            notifies_count = int(await select_db("admin", "code", "notifies_count", code))

            id = notifies_count
            await insert_db("notifies", "id", id)
            await update_db("notifies", "id", "text", id, message.text)

            await message.answer("Введите Дату:\n"
                                 "Пример: 15 10 2021", reply_markup=ReplyKeyboardRemove())
            await StateMachine.NotifyDate.set()


@dp.message_handler(state=StateMachine.NotifyDate)
async def mess(message: Message):
    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----
    else:
        check = True
        date = message.text
        try:
            date1 = int(re.sub(" ", "", date))
        except:
            check = False

        if check:
            id = int(await select_db("admin", "code", "notifies_count", code))
            day = date.split()[0]
            await update_db("notifies", "id", "day", id, day)
            month = date.split()[1]
            await update_db("notifies", "id", "month", id, month)
            year = date.split()[2]
            await update_db("notifies", "id", "year", id, year)

            await message.answer("Введите Время:\n"
                                 "Пример: 12 30")
            await StateMachine.NotifyTime.set()
        else:
            await message.answer("Неверный формат✖️ Попробуйте еще раз")


@dp.message_handler(state=StateMachine.NotifyTime)
async def mess(message: Message):
    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----
    else:
        check = True
        date = message.text
        try:
            date1 = int(re.sub(" ", "", date))
        except:
            check = False

        if check:
            id = int(await select_db("admin", "code", "notifies_count", code))
            hour = date.split()[0]
            await update_db("notifies", "id", "hour", id, hour)
            min = date.split()[1]
            await update_db("notifies", "id", "min", id, min)

            notifies_count = id + 1
            await update_db("admin", "code", "notifies_count", code, notifies_count)

            await message.answer("Уведомление успешно создано⚡️", reply_markup=AdminMenu)
            await StateMachine.Admin.set()
        else:
            await message.answer("Неверный формат✖️ Попробуйте еще раз")
