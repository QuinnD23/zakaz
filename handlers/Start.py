from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.filters import Command

# config
from data.config import code

# date
import datetime

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import AdminMenu

# ping
from utils.pinging import ping
from loader import dp


@dp.message_handler(Command("start"))
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    admin_name = str(await select_db("admin", "code", "admin_name", code))

    if user_name == admin_name:
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()

        await ping(dp)
    else:
        counter = 0
        workers_count = int(await select_db("admin", "code", "workers_count", code))
        while counter < workers_count:
            try:
                worker_name = str(await select_db("workers", "id", "worker_name", counter))
            except:
                continue
            worker_name = worker_name[1:]
            if user_name == worker_name:
                worker_name = "@" + worker_name
                await update_db("workers", "worker_name", "tele_id", worker_name, user_id)
                await message.answer("Вы успешно авторизировались!")
                break
            counter += 1
