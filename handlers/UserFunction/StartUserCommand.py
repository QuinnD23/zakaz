from aiogram import Dispatcher

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import UserMenu


async def start_user(user_id, dp: Dispatcher):

    hello_text = str(await select_db("options", "code", "hello_text", code))

    # Проверка на Полную Регистрацию
    enter_contacts_count = int(await select_db("users", "user_id", "enter_contacts_count", user_id))
    real_contacts_count = int(await select_db("counters", "code", "real_contacts_count", code))

    if enter_contacts_count == real_contacts_count:
        await dp.bot.send_message(user_id, hello_text, reply_markup=UserMenu)
        await StateMachine.User.set()
    else:
        # На всякий случай сотрем все старые Контакты
        contacts_counter = 1
        contacts_count = int(await select_db("counters", "code", "contacts_count", code))

        while contacts_counter <= contacts_count:
            user_contact_id = str(contacts_counter) + user_id
            try:
                await delete_db("userscontacts", "user_contact_id", user_contact_id)
            except:
                pass
            contacts_counter += 1

        # Регистрация
        await dp.bot.send_message(user_id, hello_text)

        contacts_counter = 1
        contacts_count = int(await select_db("counters", "code", "contacts_count", code))

        while contacts_counter <= contacts_count:
            try:
                type = str(await select_db("contactsoptions", "contact_num", "type", contacts_counter))
            except:
                contacts_counter += 1
                continue

            # Сохраняем последний введенный Контакт
            await update_db("users", "user_id", "last_enter_contact", user_id, contacts_counter)

            await dp.bot.send_message(user_id, f"Введите {type}")

            break

        await StateMachine.EnterContacts.set()
