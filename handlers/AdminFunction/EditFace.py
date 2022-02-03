from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# start_command
from handlers.CommandStart import start_command

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import MainAdminMenu, AdminMenu, BackMenu, EditContactsMenu, StopMenu


@dp.message_handler(state=StateMachine.EditFaceCommands)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start
    if message.text == "/start":
        await start_command("start", user_name, user_id, dp)
    # *****

    # back
    if message.text == "Отменить◀️":
        await start_command("back", user_name, user_id, dp)
    # *****

    if message.text == "Приветствие🤚":
        hello_text = str(await select_db("options", "code", "hello_text", code))
        await message.answer(f"🤚Текущее Приветствие:\n"
                             f"{hello_text}")
        await message.answer(f"Введите Новый текст Приветствия:", reply_markup=BackMenu)
        await StateMachine.EditHelloText.set()

    if message.text == "Рабочее Время⌚️":
        work_time_text = str(await select_db("options", "code", "work_time_text", code))
        await message.answer(f"⌚️Текущая Информация о Времени Работы:\n"
                             f"{work_time_text}")
        await message.answer(f"Введите Новый текст Времени Работы:", reply_markup=BackMenu)
        await StateMachine.EditWorkTimeText.set()

    if message.text == "Завершение☑️":
        end_text = str(await select_db("options", "code", "end_text", code))
        await message.answer(f"☑️Текущий текст Завершения:\n"
                             f"{end_text}")
        await message.answer(f"Введите Новый текст Завершения:", reply_markup=BackMenu)
        await StateMachine.EditEndText.set()

    if message.text == "Контакты📚":
        await message.answer("📚Список текущих Контактов:", reply_markup=EditContactsMenu)
        contact_num = 1
        contacts_count = int(await select_db("counters", "code", "contacts_count", code))
        del_contact_num = 1
        while contact_num <= contacts_count:
            try:
                type = str(await select_db("contactsoptions", "contact_num", "type", contact_num))
            except:
                contact_num += 1
                continue

            await message.answer(f"{del_contact_num}. {type}")

            # del update
            await update_db("contactsoptions", "contact_num", "del_contact_num", contact_num, del_contact_num)
            del_contact_num += 1

            contact_num += 1

        await StateMachine.EditContactsCommands.set()


@dp.message_handler(state=StateMachine.EditContactsCommands)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start
    if message.text == "/start":
        await start_command("start", user_name, user_id, dp)
    # *****

    # back
    if message.text == "Отменить◀️":
        await start_command("back", user_name, user_id, dp)
    # *****

    if message.text == "Добавить Контакт📚":
        await message.answer("🔖Пример: Номер телефона☎️\n"
                             "Введите Контакт, который хотите узнать у клиента:", reply_markup=BackMenu)
        await StateMachine.AddContacts.set()

    if message.text == "Удалить Контакт❌":
        await message.answer("⚡️Чтобы удалить Контакт\n"
                             "Введите Номер Контакта из текущего списка:", reply_markup=StopMenu)
        await StateMachine.DeleteContacts.set()


@dp.message_handler(state=StateMachine.AddContacts)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start
    if message.text == "/start":
        await start_command("start", user_name, user_id, dp)
    # *****

    # back
    if message.text == "Отменить◀️":
        await start_command("back", user_name, user_id, dp)
    # *****

    else:
        # Добавление контакта
        type = message.text
        try:
            await insert_db("contactsoptions", "type", type)
        except:
            pass

        # Обновление числа контактов
        contacts_count = int(await select_db("counters", "code", "contacts_count", code)) + 1
        await update_db("counters", "code", "contacts_count", code, contacts_count)

        if user_name == main_admin_name:
            await message.answer(f"📚Контакт {type} добавлен", reply_markup=MainAdminMenu)
            await StateMachine.MainAdmin.set()
        else:
            await message.answer(f"📚Контакт {type} добавлен", reply_markup=AdminMenu)
            await StateMachine.Admin.set()


@dp.message_handler(state=StateMachine.DeleteContacts)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start
    if message.text == "/start":
        await start_command("start", user_name, user_id, dp)
    # *****

    # back
    if message.text == "Отменить◀️":
        await start_command("back", user_name, user_id, dp)
    # *****

    else:
        # Проверка на число
        check_num = True
        del_contact_num = message.text
        try:
            del_contact_num = int(del_contact_num)
        except:
            check_num = False

        if check_num:
            # Проверка на существования
            check_table = True
            try:
                type = str(await select_db("contactsoptions", "del_contact_num", "type", del_contact_num))
            except:
                check_table = False

            if check_table:
                # Удаление Контакта
                await delete_db("contactsoptions", "del_contact_num", del_contact_num)

                # Уменьшение количества Контактов
                contacts_count = int(await select_db("counters", "code", "contacts_count", code)) - 1
                await update_db("counters", "code", "contacts_count", code, contacts_count)

                if user_name == main_admin_name:
                    await message.answer(f"❌Контакт {type} удален", reply_markup=MainAdminMenu)
                    await StateMachine.MainAdmin.set()
                else:
                    await message.answer(f"❌Контакт {type} удален", reply_markup=AdminMenu)
                    await StateMachine.Admin.set()
            # check table
            else:
                await message.answer("❗️Неверный формат")
        # check_num
        else:
            await message.answer("❗️Неверный формат")


@dp.message_handler(state=StateMachine.EditHelloText)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start
    if message.text == "/start":
        await start_command("start", user_name, user_id, dp)
    # *****

    # back
    if message.text == "Отменить◀️":
        await start_command("back", user_name, user_id, dp)
    # *****

    else:
        # Добавление Приветствия
        hello_text = message.text
        await update_db("options", "code", "hello_text", code, hello_text)

        if user_name == main_admin_name:
            await message.answer(f"🤚Текст Приветствия изменен:\n"
                                 f"{hello_text}", reply_markup=MainAdminMenu)
            await StateMachine.MainAdmin.set()
        else:
            await message.answer(f"🤚Текст Приветствия изменен:\n"
                                 f"{hello_text}", reply_markup=AdminMenu)
            await StateMachine.Admin.set()


@dp.message_handler(state=StateMachine.EditWorkTimeText)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start
    if message.text == "/start":
        await start_command("start", user_name, user_id, dp)
    # *****

    # back
    if message.text == "Отменить◀️":
        await start_command("back", user_name, user_id, dp)
    # *****

    else:
        # Добавление Времени Работы
        work_time_text = message.text
        await update_db("options", "code", "work_time_text", code, work_time_text)

        if user_name == main_admin_name:
            await message.answer(f"⌚️Текст Информации о Времени Работы изменен:\n"
                                 f"{work_time_text}", reply_markup=MainAdminMenu)
            await StateMachine.MainAdmin.set()
        else:
            await message.answer(f"⌚️Текст Информации о Времени Работы изменен:\n"
                                 f"{work_time_text}", reply_markup=AdminMenu)
            await StateMachine.Admin.set()


@dp.message_handler(state=StateMachine.EditEndText)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start
    if message.text == "/start":
        await start_command("start", user_name, user_id, dp)
    # *****

    # back
    if message.text == "Отменить◀️":
        await start_command("back", user_name, user_id, dp)
    # *****

    else:
        # Добавление Завершения
        end_text = message.text
        await update_db("options", "code", "end_text", code, end_text)

        if user_name == main_admin_name:
            await message.answer(f"☑️Текст Завершения изменен:\n"
                                 f"{end_text}", reply_markup=MainAdminMenu)
            await StateMachine.MainAdmin.set()
        else:
            await message.answer(f"☑️Текст Завершения изменен:\n"
                                 f"{end_text}", reply_markup=AdminMenu)
            await StateMachine.Admin.set()
