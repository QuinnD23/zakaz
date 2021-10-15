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
from kyeboards.marks import AdminMenu, EditMenu


@dp.message_handler(state=StateMachine.EditChoice)
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
            check = True
            try:
                delete_id = int(message.text)
            except:
                check = False

            if check:
                check = True
                try:
                    text = str(await select_db("notifies", "delete_id", "text", delete_id))
                except:
                    check = False
                if check:
                    year = int(await select_db("notifies", "id", "year", delete_id))
                    month = int(await select_db("notifies", "id", "month", delete_id))
                    day = int(await select_db("notifies", "id", "day", delete_id))
                    hour = int(await select_db("notifies", "id", "hour", delete_id))
                    min = int(await select_db("notifies", "id", "min", delete_id))

                    await update_db("admin", "code", "edit_notify", code, delete_id)

                    await message.answer(f"Вы выбрали:\n"
                                         f"{delete_id}. {text}"
                                         f"Дата: {day}.{month}.{year}"
                                         f"Время: {hour}:{min}", reply_markup=EditMenu)
                    await message.answer("Что будем менять?")
                    await StateMachine.EditMain.set()
                else:
                    await message.answer("Неверный формат✖️ Попробуйте еще раз")
            else:
                await message.answer("Неверный формат✖️ Попробуйте еще раз")


@dp.message_handler(state=StateMachine.EditMain)
async def mess(message: Message):
    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----

    # ----- back
    if message.text == "Отменить◀️":
        await message.answer("Возвращаю...", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----

    if message.text == "Текст":
        await message.answer("Введите новый Текст:", reply_markup=ReplyKeyboardRemove())
        await StateMachine.Text.set()

    if message.text == "Дата":
        await message.answer("Введите новую Дату:"
                             "Пример: 15 10 2021", reply_markup=ReplyKeyboardRemove())
        await StateMachine.Date.set()

    if message.text == "Время":
        await message.answer("Введите новое Время:"
                             "Пример: 12 30", reply_markup=ReplyKeyboardRemove())
        await StateMachine.Time.set()


@dp.message_handler(state=StateMachine.Text)
async def mess(message: Message):
    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----
    else:
        delete_id = int(await select_db("admin", "code", "edit_notify", code))
        await update_db("notifies", "delete_id", "text", delete_id, message.text)

        text = str(await select_db("notifies", "delete_id", "text", delete_id))
        year = int(await select_db("notifies", "id", "year", delete_id))
        month = int(await select_db("notifies", "id", "month", delete_id))
        day = int(await select_db("notifies", "id", "day", delete_id))
        hour = int(await select_db("notifies", "id", "hour", delete_id))
        min = int(await select_db("notifies", "id", "min", delete_id))

        await message.answer(f"✅ Уведомление Изменено:\n"
                             f"{delete_id}. {text}"
                             f"Дата: {day}.{month}.{year}"
                             f"Время: {hour}:{min}", reply_markup=EditMenu)
        await message.answer("Хотите изменить еще что-то?")
        await StateMachine.EditMain.set()


@dp.message_handler(state=StateMachine.Date)
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
            delete_id = int(await select_db("admin", "code", "edit_notify", code))
            day = date.split()[0]
            await update_db("notifies", "delete_id", "day", delete_id, day)
            month = date.split()[1]
            await update_db("notifies", "delete_id", "month", delete_id, month)
            year = date.split()[2]
            await update_db("notifies", "delete_id", "year", delete_id, year)

            text = str(await select_db("notifies", "delete_id", "text", delete_id))
            year = int(await select_db("notifies", "id", "year", delete_id))
            month = int(await select_db("notifies", "id", "month", delete_id))
            day = int(await select_db("notifies", "id", "day", delete_id))
            hour = int(await select_db("notifies", "id", "hour", delete_id))
            min = int(await select_db("notifies", "id", "min", delete_id))

            await message.answer(f"✅ Уведомление Изменено:\n"
                                 f"{delete_id}. {text}"
                                 f"Дата: {day}.{month}.{year}"
                                 f"Время: {hour}:{min}", reply_markup=EditMenu)
            await message.answer("Хотите изменить еще что-то?")
            await StateMachine.EditMain.set()
        else:
            await message.answer("Неверный формат✖️ Попробуйте еще раз")


@dp.message_handler(state=StateMachine.Time)
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
            delete_id = int(await select_db("admin", "code", "edit_notify", code))
            hour = date.split()[0]
            await update_db("notifies", "delete_id", "hour", delete_id, hour)
            min = date.split()[1]
            await update_db("notifies", "delete_id", "min", delete_id, min)

            text = str(await select_db("notifies", "delete_id", "text", delete_id))
            year = int(await select_db("notifies", "id", "year", delete_id))
            month = int(await select_db("notifies", "id", "month", delete_id))
            day = int(await select_db("notifies", "id", "day", delete_id))
            hour = int(await select_db("notifies", "id", "hour", delete_id))
            min = int(await select_db("notifies", "id", "min", delete_id))

            await message.answer(f"✅ Уведомление Изменено:\n"
                                 f"{delete_id}. {text}"
                                 f"Дата: {day}.{month}.{year}"
                                 f"Время: {hour}:{min}", reply_markup=EditMenu)
            await message.answer("Хотите изменить еще что-то?")
            await StateMachine.EditMain.set()
        else:
            await message.answer("Неверный формат✖️ Попробуйте еще раз")
