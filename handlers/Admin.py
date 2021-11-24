from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.filters import Command

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import AdminMenu, BackMenu, NotifyMenu


@dp.message_handler(state=StateMachine.Admin)
async def mess(message: Message):

    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
    # -----

    if message.text == "Добавить сотрудника✅":
        await message.answer("Введите Ник Телеграм сотрудника:\n"
                             "Пример: @kquinn1", reply_markup=BackMenu)
        await StateMachine.Add.set()

    if message.text == "Удалить сотрудника❌":
        await message.answer("Список текущих сотрудников:", reply_markup=BackMenu)
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

        await message.answer("Введите номер сотрудника, которого хотите удалить:")
        await StateMachine.Delete.set()

    if message.text == "Создать уведомление⚡️":
        await message.answer("Выберите тип уведомления:", reply_markup=NotifyMenu)
        await StateMachine.NotifyChoice.set()

    if message.text == "Редактировать уведомление✏️":
        await message.answer("Выберите тип уведомления:", reply_markup=NotifyMenu)
        await StateMachine.EditMainChoice.set()


@dp.message_handler(state=StateMachine.EditMainChoice)
async def mess(message: Message):

    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
    # -----

    # ----- back
    if message.text == "Отменить◀️":
        await message.answer("Возвращаю...", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----

    if message.text == "День недели☀️":
        await message.answer("⚡️Список текущих уведомлений:", reply_markup=BackMenu)
        counter = 0
        delete_id = 1
        notifies_count = int(await select_db("admin", "code", "notifies_week_count", code))
        while counter < notifies_count:
            try:
                text = str(await select_db("notifiesweek", "id", "text", counter))
            except:
                counter += 1
                continue
            named_day = str(await select_db("notifiesweek", "id", "named_day", counter))
            if named_day == "Monday":
                named_day = "пн"
            if named_day == "Tuesday":
                named_day = "вт"
            if named_day == "Wednesday":
                named_day = "ср"
            if named_day == "Thursday":
                named_day = "чт"
            if named_day == "Friday":
                named_day = "пт"
            if named_day == "Saturday":
                named_day = "сб"
            if named_day == "Sunday":
                named_day = "вс"
            hour = str(await select_db("notifiesweek", "id", "hour", counter))
            min = str(await select_db("notifiesweek", "id", "min", counter))

            all_members = ""
            members_counter = 0
            members_count = int(await select_db("notifiesweek", "id", "members_count", counter))
            while members_counter < members_count:
                id_member = str(counter) + '#' + str(members_counter)
                try:
                    member_name = str(await select_db("notifiesmembersweek", "id_member", "member_name", id_member))
                except:
                    members_counter += 1
                    continue
                all_members = all_members + member_name + ", "
                members_counter += 1

            all_members = all_members[:-2]

            await message.answer(f"{delete_id}💥{text}\n"
                                 f"День недели - {named_day}\n"
                                 f"Время - {hour}:{min}\n"
                                 f"Сотрудники - {all_members}")
            await update_db("notifiesweek", "id", "delete_id", counter, delete_id)
            counter += 1
            delete_id += 1

        await message.answer("Введите номер уведомления, которое хотите изменить:")
        await StateMachine.EditChoiceWeek.set()

    if message.text == "Конкретная дата🌩":
        await message.answer("⚡️Список текущих уведомлений:", reply_markup=BackMenu)
        counter = 0
        delete_id = 1
        notifies_count = int(await select_db("admin", "code", "notifies_count", code))
        while counter < notifies_count:
            try:
                text = str(await select_db("notifies", "id", "text", counter))
            except:
                counter += 1
                continue
            year = str(await select_db("notifies", "id", "year", counter))
            month = str(await select_db("notifies", "id", "month", counter))
            day = str(await select_db("notifies", "id", "day", counter))
            hour = str(await select_db("notifies", "id", "hour", counter))
            min = str(await select_db("notifies", "id", "min", counter))

            all_members = ""
            members_counter = 0
            members_count = int(await select_db("notifies", "id", "members_count", counter))
            while members_counter < members_count:
                id_member = str(counter) + '#' + str(members_counter)
                try:
                    member_name = str(await select_db("notifiesmembers", "id_member", "member_name", id_member))
                except:
                    members_counter += 1
                    continue
                all_members = all_members + member_name + ", "
                members_counter += 1

            all_members = all_members[:-2]

            await message.answer(f"{delete_id}💥{text}\n"
                                 f"Дата - {day}.{month}.{year}\n"
                                 f"Время - {hour}:{min}\n"
                                 f"Сотрудники - {all_members}")
            await update_db("notifies", "id", "delete_id", counter, delete_id)
            counter += 1
            delete_id += 1

        await message.answer("Введите номер уведомления, которое хотите изменить:")
        await StateMachine.EditChoice.set()


@dp.message_handler(state=StateMachine.NotifyChoice)
async def mess(message: Message):

    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
    # -----

    # ----- back
    if message.text == "Отменить◀️":
        await message.answer("Возвращаю...", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----

    if message.text == "День недели☀️":
        await message.answer("Введите Текст уведомления:", reply_markup=ReplyKeyboardRemove())
        await StateMachine.NotifyTextWeek.set()

    if message.text == "Конкретная дата🌩":
        await message.answer("Введите Текст уведомления:", reply_markup=ReplyKeyboardRemove())
        await StateMachine.NotifyText.set()
