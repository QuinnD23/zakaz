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
from kyeboards.marks import AdminMenu, EditDayMenu, AddRemoveMenu, MembersMenu


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
                    year = str(await select_db("notifies", "delete_id", "year", delete_id))
                    month = str(await select_db("notifies", "delete_id", "month", delete_id))
                    day = str(await select_db("notifies", "delete_id", "day", delete_id))
                    hour = str(await select_db("notifies", "delete_id", "hour", delete_id))
                    min = str(await select_db("notifies", "delete_id", "min", delete_id))

                    all_members = ""
                    members_counter = 0
                    members_count = int(await select_db("notifies", "delete_id", "members_count", delete_id))
                    while members_counter < members_count:
                        id_member = str(await select_db("notifies", "delete_id", "id", delete_id)) + '#' + str(members_counter)
                        try:
                            member_name = str(await select_db("notifiesmembers", "id_member", "member_name", id_member))
                        except:
                            members_counter += 1
                            continue
                        all_members = all_members + member_name + ", "
                        members_counter += 1

                    all_members = all_members[:-2]

                    await update_db("admin", "code", "edit_notify", code, delete_id)

                    await message.answer(f"Вы выбрали:\n"
                                         f"{delete_id}💥{text}\n"
                                         f"Дата - {day}.{month}.{year}\n"
                                         f"Время - {hour}:{min}\n"
                                         f"Сотрудники - {all_members}", reply_markup=EditDayMenu)
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

    if message.text == "Текст✏️":
        await message.answer("✏️ Введите новый Текст", reply_markup=ReplyKeyboardRemove())
        await StateMachine.Text.set()

    if message.text == "Дата🗓":
        await message.answer("🗓 Введите новую Дату\n"
                             "Пример - 15 10 2021", reply_markup=ReplyKeyboardRemove())
        await StateMachine.Date.set()

    if message.text == "Время🕐":
        await message.answer("🕐 Введите новое Время\n"
                             "Пример - 12 30", reply_markup=ReplyKeyboardRemove())
        await StateMachine.Time.set()

    if message.text == "Cотрудники👨":
        await message.answer("👨 Выберите действие:", reply_markup=AddRemoveMenu)
        await StateMachine.MembersChoice.set()

    if message.text == "Удалить❌":
        delete_id = int(await select_db("admin", "code", "edit_notify", code))

        members_counter = 0
        members_count = int(await select_db("notifies", "delete_id", "members_count", delete_id))
        while members_counter < members_count:
            id_member = str(await select_db("notifies", "delete_id", "id", delete_id)) + '#' + str(members_counter)
            try:
                member_name = str(await select_db("notifiesmembers", "id_member", "member_name", id_member))
            except:
                members_counter += 1
                continue
            await delete_db("notifiesmembers", "id_member", id_member)
            members_counter += 1

        await delete_db("notifies", "delete_id", delete_id)

        await message.answer("❌ Уведомление удалено", reply_markup=AdminMenu)
        await StateMachine.Admin.set()


@dp.message_handler(state=StateMachine.MembersChoice)
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

    if message.text == "Добавить✅":
        delete_id = int(await select_db("admin", "code", "edit_notify", code))

        all_members = ""
        members_counter = 0
        members_count = int(await select_db("notifies", "delete_id", "members_count", delete_id))
        while members_counter < members_count:
            id_member = str(await select_db("notifies", "delete_id", "id", delete_id)) + '#' + str(members_counter)
            try:
                member_name = str(await select_db("notifiesmembers", "id_member", "member_name", id_member))
            except:
                members_counter += 1
                continue
            all_members = all_members + member_name + ", "
            members_counter += 1

        all_members = all_members[:-2]

        await message.answer("👨 Выберите сотрудников:")

        counter = 0
        delete_id_worker = 1
        workers_count = int(await select_db("admin", "code", "workers_count", code))
        while counter < workers_count:
            try:
                worker_name = str(await select_db("workers", "id", "worker_name", counter))
            except:
                counter += 1
                continue
            if all_members.find(worker_name) == -1:
                await message.answer(f"{delete_id_worker}. {worker_name}")
                await update_db("workers", "id", "delete_id", counter, delete_id_worker)
                delete_id_worker += 1
            counter += 1

        await message.answer("Введите номер сотрудника, которому хотите отправить уведомление:", reply_markup=MembersMenu)
        await message.answer("Когда будут выбраны все сотрудники, нажмите - Стоп⛔️")
        await StateMachine.MembersAdd.set()

    if message.text == "Удалить❌":
        await message.answer("👨 Выберите сотрудников:")

        delete_id = int(await select_db("admin", "code", "edit_notify", code))

        counter_members = 0
        delete_id_member = 1
        members_count = int(await select_db("notifies", "delete_id", "members_count", delete_id))
        while counter_members < members_count:
            id_member = str(await select_db("notifies", "delete_id", "id", delete_id)) + '#' + str(counter_members)
            try:
                member_name = str(await select_db("notifiesmembers", "id_member", "member_name", id_member))
            except:
                counter_members += 1
                continue

            await message.answer(f"{delete_id_member}. {member_name}")
            delete_id_member_table = str(delete_id) + '#' + str(delete_id_member)
            await update_db("notifiesmembers", "id_member", "delete_id", id_member, delete_id_member_table)
            delete_id_member += 1
            counter_members += 1

        await message.answer("Введите номер сотрудника, которому хотите удалить❌:", reply_markup=MembersMenu)
        await message.answer("Когда будут выбраны все сотрудники, нажмите - Стоп⛔️")

        await StateMachine.MembersRemove.set()


@dp.message_handler(state=StateMachine.MembersAdd)
async def mess(message: Message):
    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----
    else:
        if message.text == "Стоп⛔️":
            delete_id = int(await select_db("admin", "code", "edit_notify", code))

            all_members = ""
            members_counter = 0
            members_count = int(await select_db("notifies", "delete_id", "members_count", delete_id))
            while members_counter < members_count:
                id_member = str(await select_db("notifies", "delete_id", "id", delete_id)) + '#' + str(members_counter)
                try:
                    member_name = str(await select_db("notifiesmembers", "id_member", "member_name", id_member))
                except:
                    members_counter += 1
                    continue
                all_members = all_members + member_name + ", "
                members_counter += 1

            all_members = all_members[:-2]

            text = str(await select_db("notifies", "delete_id", "text", delete_id))
            year = str(await select_db("notifies", "delete_id", "year", delete_id))
            month = str(await select_db("notifies", "delete_id", "month", delete_id))
            day = str(await select_db("notifies", "delete_id", "day", delete_id))
            hour = str(await select_db("notifies", "delete_id", "hour", delete_id))
            min = str(await select_db("notifies", "delete_id", "min", delete_id))

            await message.answer(f"Уведомление Изменено:\n"
                                 f"{delete_id}💥{text}\n"
                                 f"Дата - {day}.{month}.{year}\n"
                                 f"Время - {hour}:{min}\n"
                                 f"Сотрудники - {all_members}", reply_markup=EditDayMenu)
            await message.answer("Хотите изменить еще что-то?")

            await StateMachine.EditMain.set()
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
                    id_notify = int(await select_db("admin", "code", "edit_notify", code))
                    id_member = str(await select_db("notifies", "delete_id", "id", id_notify)) + '#' + str(await select_db("notifies", "delete_id", "members_count", id_notify))

                    await insert_db("notifiesmembers", "id_member", id_member)

                    await update_db("notifiesmembers", "id_member", "member_name", id_member, member_name)

                    await message.answer(f"✅ {member_name}")

                    members_count = int(await select_db("notifies", "delete_id", "members_count", id_notify)) + 1
                    await update_db("notifies", "delete_id", "members_count", id_notify, members_count)

                    await update_db("workers", "delete_id", "delete_id", delete_id, -1)
                else:
                    await message.answer("Неверный формат✖️ Попробуйте еще раз")
            else:
                await message.answer("Неверный формат✖️ Попробуйте еще раз")


@dp.message_handler(state=StateMachine.MembersRemove)
async def mess(message: Message):
    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----
    else:
        if message.text == "Стоп⛔️":
            delete_id = int(await select_db("admin", "code", "edit_notify", code))

            all_members = ""
            members_counter = 0
            members_count = int(await select_db("notifies", "delete_id", "members_count", delete_id))
            while members_counter < members_count:
                id_member = str(await select_db("notifies", "delete_id", "id", delete_id)) + '#' + str(members_counter)
                try:
                    member_name = str(await select_db("notifiesmembers", "id_member", "member_name", id_member))
                except:
                    members_counter += 1
                    continue
                all_members = all_members + member_name + ", "
                members_counter += 1

            all_members = all_members[:-2]

            text = str(await select_db("notifies", "delete_id", "text", delete_id))
            year = str(await select_db("notifies", "delete_id", "year", delete_id))
            month = str(await select_db("notifies", "delete_id", "month", delete_id))
            day = str(await select_db("notifies", "delete_id", "day", delete_id))
            hour = str(await select_db("notifies", "delete_id", "hour", delete_id))
            min = str(await select_db("notifies", "delete_id", "min", delete_id))

            await message.answer(f"Уведомление Изменено:\n"
                                 f"{delete_id}💥{text}\n"
                                 f"Дата - {day}.{month}.{year}\n"
                                 f"Время - {hour}:{min}\n"
                                 f"Сотрудники - {all_members}", reply_markup=EditDayMenu)
            await message.answer("Хотите изменить еще что-то?")

            await StateMachine.EditMain.set()
        else:
            delete_id = int(await select_db("admin", "code", "edit_notify", code))

            check = True
            try:
                delete_id_member = int(message.text)
            except:
                check = False

            if check:
                delete_id_member = str(await select_db("notifies", "delete_id", "id", delete_id)) + '#' + str(delete_id_member)
                check = True
                try:
                    member_name = str(await select_db("notifiesmembers", "delete_id", "member_name", delete_id_member))
                except:
                    check = False
                if check:
                    await delete_db("notifiesmembers", "delete_id", delete_id_member)
                    await message.answer(f"❌ {member_name} удален")
                else:
                    await message.answer("Неверный формат✖️ Попробуйте еще раз")
            else:
                await message.answer("Неверный формат✖️ Попробуйте еще раз")


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
        year = str(await select_db("notifies", "delete_id", "year", delete_id))
        month = str(await select_db("notifies", "delete_id", "month", delete_id))
        day = str(await select_db("notifies", "delete_id", "day", delete_id))
        hour = str(await select_db("notifies", "delete_id", "hour", delete_id))
        min = str(await select_db("notifies", "delete_id", "min", delete_id))

        await message.answer(f"Уведомление Изменено:\n"
                             f"{delete_id}💥{text}\n"
                             f"Дата - {day}.{month}.{year}\n"
                             f"Время - {hour}:{min}", reply_markup=EditDayMenu)
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
            day = str(date.split()[0])
            await update_db("notifies", "delete_id", "day", delete_id, day)
            month = str(date.split()[1])
            await update_db("notifies", "delete_id", "month", delete_id, month)
            year = str(date.split()[2])
            await update_db("notifies", "delete_id", "year", delete_id, year)

            text = str(await select_db("notifies", "delete_id", "text", delete_id))
            year = str(await select_db("notifies", "delete_id", "year", delete_id))
            month = str(await select_db("notifies", "delete_id", "month", delete_id))
            day = str(await select_db("notifies", "delete_id", "day", delete_id))
            hour = str(await select_db("notifies", "delete_id", "hour", delete_id))
            min = str(await select_db("notifies", "delete_id", "min", delete_id))

            await message.answer(f"Уведомление Изменено:\n"
                                 f"{delete_id}💥{text}\n"
                                 f"Дата - {day}.{month}.{year}\n"
                                 f"Время - {hour}:{min}", reply_markup=EditDayMenu)
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
            hour = str(date.split()[0])
            await update_db("notifies", "delete_id", "hour", delete_id, hour)
            min = str(date.split()[1])
            await update_db("notifies", "delete_id", "min", delete_id, min)

            text = str(await select_db("notifies", "delete_id", "text", delete_id))
            year = str(await select_db("notifies", "delete_id", "year", delete_id))
            month = str(await select_db("notifies", "delete_id", "month", delete_id))
            day = str(await select_db("notifies", "delete_id", "day", delete_id))
            hour = str(await select_db("notifies", "delete_id", "hour", delete_id))
            min = str(await select_db("notifies", "delete_id", "min", delete_id))

            await message.answer(f"Уведомление Изменено:\n"
                                 f"{delete_id}💥{text}\n"
                                 f"Дата - {day}.{month}.{year}\n"
                                 f"Время - {hour}:{min}", reply_markup=EditDayMenu)
            await message.answer("Хотите изменить еще что-то?")
            await StateMachine.EditMain.set()
        else:
            await message.answer("Неверный формат✖️ Попробуйте еще раз")
