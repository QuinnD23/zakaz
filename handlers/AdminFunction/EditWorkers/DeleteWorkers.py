from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import MainAdminMenu, AdminMenu


@dp.message_handler(state=StateMachine.DeleteWorkers)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start and back
    if message.text == "/start" or message.text == "Отменить◀️":
        if user_name == main_admin_name:
            await message.answer("Приветствую тебя, ⭐️Главный Администратор!", reply_markup=MainAdminMenu)
            await StateMachine.MainAdmin.set()
        else:
            await message.answer("Приветствую тебя, 💫Администратор!", reply_markup=AdminMenu)
            await StateMachine.Admin.set()
    # *****

    else:
        # Проверка на число
        check_num = True
        del_worker_num = message.text
        try:
            del_worker_num = int(del_worker_num)
        except:
            check_num = False

        if check_num:
            # Проверка на существования
            check_table = True
            try:
                worker_name = str(await select_db("workers", "del_worker_num", "worker_name", del_worker_num))
            except:
                check_table = False

            if check_table:
                await delete_db("workers", "del_worker_num", del_worker_num)

                if user_name == main_admin_name:
                    await message.answer(f"❌Сотрудник @{worker_name} удален", reply_markup=MainAdminMenu)
                    await StateMachine.MainAdmin.set()
                else:
                    await message.answer(f"❌Сотрудник @{worker_name} удален", reply_markup=AdminMenu)
                    await StateMachine.Admin.set()
            # check table
            else:
                await message.answer("❗️Неверный формат")
        # check_num
        else:
            await message.answer("❗️Неверный формат")
