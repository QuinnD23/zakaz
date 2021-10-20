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
from kyeboards.marks import AdminMenu, MembersMenu


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

            await message.answer("🗓 Введите Дату\n"
                                 "Пример - 15 10 2021", reply_markup=ReplyKeyboardRemove())
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
            day = str(date.split()[0])
            await update_db("notifies", "id", "day", id, day)
            month = str(date.split()[1])
            await update_db("notifies", "id", "month", id, month)
            year = str(date.split()[2])
            await update_db("notifies", "id", "year", id, year)

            await message.answer("🕐 Введите Время\n"
                                 "Пример - 12 30")
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
            hour = str(date.split()[0])
            await update_db("notifies", "id", "hour", id, hour)
            min = str(date.split()[1])
            await update_db("notifies", "id", "min", id, min)

            await message.answer("👨 Выберите сотрудников:")

            counter = 0
            delete_id = 1
            workers_count = int(await select_db("admin", "code", "workers_count", code))
            while counter < workers_count:
                try:
                    worker_name = str(await select_db("workers", "id", "worker_name", counter))
                except:
                    counter += 1
                    continue
                await message.answer(f"{delete_id}. {worker_name}")
                await update_db("workers", "id", "delete_id", counter, delete_id)
                counter += 1
                delete_id += 1

            await message.answer("Введите номер сотрудника, которому хотите отправить уведомление:", reply_markup=MembersMenu)
            await message.answer("Когда будут выбраны все сотрудники, нажмите - Стоп⛔️")
            await StateMachine.NotifyMembers.set()
        else:
            await message.answer("Неверный формат✖️ Попробуйте еще раз")


@dp.message_handler(state=StateMachine.NotifyMembers)
async def mess(message: Message):
    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----
    else:
        if message.text == "Стоп⛔️":
            await message.answer("Уведомление успешно создано⚡️", reply_markup=AdminMenu)

            notifies_count = id + 1
            await update_db("admin", "code", "notifies_count", code, notifies_count)

            await StateMachine.Admin.set()
        else:
            check = True
            try:
                delete_id = int(message.text)
            except:
                check = False

            if check:
                check = True
                try:
                    member_name = str(await select_db("workers", "delete_id", "worker_name", delete_id))
                except:
                    check = False
                if check:
                    member_id = str(await select_db("workers", "delete_id", "tele_id", delete_id))
                    id_notify = int(await select_db("admin", "code", "notifies_count", code))
                    id = int(await select_db("notifies", "id", "members_count", id_notify))
                    await insert_db("notifiesmembers", "id", id)

                    await update_db("notifiesmembers", "id", "id_notify", id, id_notify)
                    await update_db("notifiesmembers", "id", "member_name", id, member_name)
                    await update_db("notifiesmembers", "id", "member_id", id, member_id)

                    await message.answer(f"✅ @{member_name}")

                    id += 1
                    await update_db("notifies", "id", "members_count", id_notify, id)
                else:
                    await message.answer("Неверный формат✖️ Попробуйте еще раз")
            else:
                await message.answer("Неверный формат✖️ Попробуйте еще раз")
