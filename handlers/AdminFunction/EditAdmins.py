from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import MainAdminMenu, BackMenu


@dp.message_handler(state=StateMachine.EditAdminsCommands)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start and back
    if message.text == "/start" or message.text == "Отменить◀️":
        await message.answer("Приветствую тебя, ⭐️Главный Администратор!", reply_markup=MainAdminMenu)
        await StateMachine.MainAdmin.set()
    # *****

    if message.text == "Добавить Администратора💫":
        await message.answer("🔖Пример: @kquinn1\n"
                             "Введите Telegram Ник Администратора:", reply_markup=BackMenu)
        await StateMachine.AddAdmins.set()

    if message.text == "Удалить Администратора❌":
        await message.answer("⚡️Чтобы удалить Администратора\n"
                             "Введите Номер Администратора из текущего списка:", reply_markup=BackMenu)
        await StateMachine.DeleteAdmins.set()


@dp.message_handler(state=StateMachine.AddAdmins)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start and back
    if message.text == "/start" or message.text == "Отменить◀️":
        await message.answer("Приветствую тебя, ⭐️Главный Администратор!", reply_markup=MainAdminMenu)
        await StateMachine.MainAdmin.set()
    # *****

    else:
        # Добавление администратора
        admin_name = message.text
        admin_name = admin_name[1:]
        try:
            await insert_db("admins", "admin_name", admin_name)
        except:
            pass

        # Обновление числа администраторов
        admins_count = int(await select_db("counters", "code", "admins_count", code)) + 1
        await update_db("counters", "code", "admins_count", code, admins_count)

        await message.answer(f"💫Администратор @{admin_name} добавлен", reply_markup=MainAdminMenu)
        await StateMachine.MainAdmin.set()


@dp.message_handler(state=StateMachine.DeleteAdmins)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start and back
    if message.text == "/start" or message.text == "Отменить◀️":
        await message.answer("Приветствую тебя, ⭐️Главный Администратор!", reply_markup=MainAdminMenu)
        await StateMachine.MainAdmin.set()
    # *****

    else:
        # Проверка на число
        check_num = True
        del_admin_num = message.text
        try:
            del_admin_num = int(del_admin_num)
        except:
            check_num = False

        if check_num:
            # Проверка на существования
            check_table = True
            try:
                admin_name = str(await select_db("admins", "del_admin_num", "admin_name", del_admin_num))
            except:
                check_table = False

            if check_table:
                await delete_db("admins", "del_admin_num", del_admin_num)

                await message.answer(f"❌Администратор @{admin_name} удален", reply_markup=MainAdminMenu)
                await StateMachine.MainAdmin.set()
            # check table
            else:
                await message.answer("❗️Неверный формат")
        # check_num
        else:
            await message.answer("❗️Неверный формат")
