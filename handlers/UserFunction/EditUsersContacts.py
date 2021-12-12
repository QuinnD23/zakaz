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
from kyeboards.marks import UserMenu, BackMenu


@dp.message_handler(state=StateMachine.User)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start
    if message.text == "/start" or message.text == "Назад◀️":
        await start_command(user_name, user_id, dp)
    # *****

    if message.text == "Изменить Контакт📘":
        await message.answer("⚡️Чтобы изменить Контакт\n"
                             "Введите Номер Контакта из списка:", reply_markup=BackMenu)
        await StateMachine.DelNumContactWait.set()


@dp.message_handler(state=StateMachine.DelNumContactWait)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start and back
    if message.text == "/start" or message.text == "Отменить◀️":
        await start_command(user_name, user_id, dp)
    # *****

    else:
        # Проверка на число
        check_num = True
        del_user_contact_id_num = message.text
        try:
            del_user_contact_id_num = int(del_user_contact_id_num)
        except:
            check_num = False

        if check_num:
            # Проверка на существования
            del_user_contact_id = str(del_user_contact_id_num) + '#' + user_id

            check_table = True
            try:
                info = str(await select_db("userscontacts", "del_user_contact_id", "info", del_user_contact_id))
            except:
                check_table = False

            if check_table:
                # Запишем id Контакта, который изменяем
                user_contact_id = str(await select_db("userscontacts", "del_user_contact_id", "user_contact_id", del_user_contact_id))
                await update_db("users", "user_id", "user_contact_id", user_id, user_contact_id)

                await message.answer(f"🔖Выбранный Контакт: {info}\n"
                                     f"📘Введите Новую Информацию:")
                await StateMachine.NewContactWait.set()
            # check table
            else:
                await message.answer("❗️Неверный формат")
        # check_num
        else:
            await message.answer("❗️Неверный формат")


@dp.message_handler(state=StateMachine.NewContactWait)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start and back
    if message.text == "/start" or message.text == "Отменить◀️":
        await start_command(user_name, user_id, dp)
    # *****

    else:
        # Обновление Контакта
        info = message.text
        user_contact_id = str(await select_db("users", "user_id", "user_contact_id", user_id))
        await update_db("userscontacts", "user_contact_id", "info", user_contact_id, info)

        await message.answer("📘Контакт обновлен", reply_markup=UserMenu)

        await StateMachine.User.set()
