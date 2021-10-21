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


@dp.message_handler(state=StateMachine.NotifyTextWeek)
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
            notifies_week_count = int(await select_db("admin", "code", "notifies_week_count", code))

            id = notifies_week_count
            await insert_db("notifiesweek", "id", id)
            await update_db("notifiesweek", "id", "text", id, message.text)

            await message.answer("☀️ Введите День недели\n"
                                 "Пример - пн, вт, ср, чт, пт, сб, вс", reply_markup=ReplyKeyboardRemove())
            await StateMachine.NotifyDateWeek.set()


@dp.message_handler(state=StateMachine.NotifyDateWeek)
async def mess(message: Message):
    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----
    else:
        check = True
        date = message.text

        if date == "пн" or date == "вт" or date == "ср" or date == "чт" or date == "пт" or date == "сб" or date == "вс":
            id = int(await select_db("admin", "code", "notifies_week_count", code))
            if date == "пн":
                await update_db("notifiesweek", "id", "named_day", id, "Monday")
            if date == "вт":
                await update_db("notifiesweek", "id", "named_day", id, "Tuesday")
            if date == "ср":
                await update_db("notifiesweek", "id", "named_day", id, "Wednesday")
            if date == "чт":
                await update_db("notifiesweek", "id", "named_day", id, "Thursday")
            if date == "пт":
                await update_db("notifiesweek", "id", "named_day", id, "Friday")
            if date == "сб":
                await update_db("notifiesweek", "id", "named_day", id, "Saturday")
            if date == "вс":
                await update_db("notifiesweek", "id", "named_day", id, "Sunday")

            await message.answer("🕐 Введите Время\n"
                                 "Пример - 12 30")
            await StateMachine.NotifyTimeWeek.set()
        else:
            await message.answer("Неверный формат✖️ Попробуйте еще раз")


@dp.message_handler(state=StateMachine.NotifyTimeWeek)
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
            id = int(await select_db("admin", "code", "notifies_week_count", code))
            hour = str(date.split()[0])
            await update_db("notifiesweek", "id", "hour", id, hour)
            min = str(date.split()[1])
            await update_db("notifiesweek", "id", "min", id, min)

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
            await StateMachine.NotifyMembersWeek.set()
        else:
            await message.answer("Неверный формат✖️ Попробуйте еще раз")


@dp.message_handler(state=StateMachine.NotifyMembersWeek)
async def mess(message: Message):
    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----
    else:
        if message.text == "Стоп⛔️":
            await message.answer("Уведомление успешно создано⚡️", reply_markup=AdminMenu)

            notifies_week_count = int(await select_db("admin", "code", "notifies_week_count", code)) + 1
            await update_db("admin", "code", "notifies_count", code, notifies_week_count)

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
                    id_notify = int(await select_db("admin", "code", "notifies_week_count", code))
                    id_member = str(id_notify) + '#' + str(await select_db("notifiesweek", "id", "members_count", id_notify))

                    await insert_db("notifiesmembersweek", "id_member", id_member)

                    await update_db("notifiesmembersweek", "id_member", "member_name", id_member, member_name)

                    await message.answer(f"✅ {member_name}")

                    members_count = int(await select_db("notifiesweek", "id", "members_count", id_notify)) + 1
                    await update_db("notifiesweek", "id", "members_count", id_notify, members_count)

                    await update_db("workers", "delete_id", "delete_id", delete_id, -1)
                else:
                    await message.answer("Неверный формат✖️ Попробуйте еще раз")
            else:
                await message.answer("Неверный формат✖️ Попробуйте еще раз")
