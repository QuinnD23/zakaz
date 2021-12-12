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
from kyeboards.marks import UserMenu


@dp.message_handler(state=StateMachine.EnterContacts)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start and back
    if message.text == "/start":
        await start_command(user_name, user_id, dp)
    # *****

    else:
        last_enter_contact = int(await select_db("users", "user_id", "last_enter_contact", user_id))

        user_contact_id = str(last_enter_contact) + '#' + user_id
        await insert_db("userscontacts", "user_contact_id")

        info = message.text
        await update_db("userscontacts", "user_contact_id", "info", user_contact_id, info)

        # Обновим кол-во введенных Контактов
        enter_contacts_count = int(await select_db("users", "user_id", "enter_contacts_count", user_id)) + 1
        await update_db("users", "user_id", "enter_contacts_count", user_id, enter_contacts_count)

        # Ищем следующий сушествующий Контакт
        contact_num = last_enter_contact + 1
        contacts_count = int(await select_db("counters", "code", "contacts_count", code))

        while contact_num <= contacts_count:
            try:
                type = str(await select_db("contactsoptions", "contact_num", "type", contact_num))
            except:
                contact_num += 1

            # Сохраняем последний введенный Контакт
            await update_db("users", "user_id", "last_enter_contact", user_id, contact_num)

            await message.answer(f"Введите {type}")

            break

        if contact_num > contacts_count:
            await message.answer("🥳Регистрация пройдена", reply_markup=UserMenu)
            await StateMachine.User.set()
