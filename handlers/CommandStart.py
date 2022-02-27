from aiogram import Dispatcher

from aiogram.types import Message, ReplyKeyboardRemove

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import MainAdminMenu, AdminMenu, UserMenu


async def start_command(tag, user_name, user_id, dp: Dispatcher):
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    if user_name == main_admin_name:
        await update_db("mainadmin", "code", "main_admin_id", code, user_id)

        if tag == "start":
            await dp.bot.send_message(user_id, "Приветствую тебя, ⭐️Главный Администратор!", reply_markup=MainAdminMenu)
        else:
            await dp.bot.send_message(user_id, "🌀Возвращаю", reply_markup=MainAdminMenu)
        await StateMachine.MainAdmin.set()
    else:
        # Проверка Админстратора
        user = True
        admin_num = 1
        admins_count = int(await select_db("counters", "code", "admins_count", code))
        while admin_num <= admins_count:
            try:
                admin_name = str(await select_db("admins", "admin_num", "admin_name", admin_num))
            except:
                admin_num += 1
                continue

            if user_name == admin_name:
                await update_db("admins", "admin_num", "admin_id", admin_num, user_id)

                if tag == "start":
                    await dp.bot.send_message(user_id, "Приветствую тебя, 💫Администратор!", reply_markup=AdminMenu)
                else:
                    await dp.bot.send_message(user_id, "🌀Возвращаю", reply_markup=AdminMenu)
                await StateMachine.Admin.set()

                user = False
                break

            admin_num += 1

        # Пользователь
        if user:
            try:
                await insert_db("users", "user_id", user_id)
            except:
                pass
            await update_db("users", "user_id", "user_name", user_id, user_name)

            hello_text = str(await select_db("options", "code", "hello_text", code))

            # Проверка на Полную Регистрацию
            enter_contacts_count = int(await select_db("users", "user_id", "enter_contacts_count", user_id))
            real_contacts_count = int(await select_db("counters", "code", "real_contacts_count", code))

            if enter_contacts_count == real_contacts_count:
                if tag == "start":
                    await dp.bot.send_message(user_id, hello_text, reply_markup=UserMenu)
                else:
                    await dp.bot.send_message(user_id, "🌀Возвращаю", reply_markup=UserMenu)
                await StateMachine.User.set()
            else:
                # На всякий случай сотрем все старые Контакты
                contact_num = 1
                contacts_count = int(await select_db("counters", "code", "contacts_count", code))

                while contact_num <= contacts_count:
                    user_contact_id = str(contact_num) + '#' + user_id
                    try:
                        await delete_db("userscontacts", "user_contact_id", user_contact_id)
                    except:
                        pass
                    contact_num += 1

                # Обнулим счетчик введенных контактов
                await update_db("users", "user_id", "enter_contacts_count", user_id, 0)

                # Регистрация
                if tag == "start":
                    await dp.bot.send_message(user_id, hello_text, reply_markup=ReplyKeyboardRemove())
                else:
                    await dp.bot.send_message(user_id, "🌀Возвращаю", reply_markup=ReplyKeyboardRemove())

                contact_num = 1
                contacts_count = int(await select_db("counters", "code", "contacts_count", code))

                while contact_num <= contacts_count:
                    try:
                        type = str(await select_db("contactsoptions", "contact_num", "type", contact_num))
                    except:
                        contact_num += 1
                        continue

                    # Сохраняем последний введенный Контакт
                    await update_db("users", "user_id", "last_enter_contact", user_id, contact_num)

                    if tag == "start":
                        await dp.bot.send_message(user_id, f"Введите {type}", reply_markup=ReplyKeyboardRemove())
                    else:
                        await dp.bot.send_message(user_id, "🌀Возвращаю", reply_markup=ReplyKeyboardRemove())

                    break

                await StateMachine.EnterContacts.set()
