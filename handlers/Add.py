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
from kyeboards.marks import AdminMenu


@dp.message_handler(state=StateMachine.Add)
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
            worker_name = message.text
            workers_count = int(await select_db("admin", "code", "workers_count", code))
            await insert_db("workers", "id", workers_count)
            await update_db("workers", "id", "worker_name", workers_count, worker_name)
            workers_count += 1
            await update_db("admin", "code", "workers_count", code, workers_count)
            await message.answer(f"✅ {worker_name} добавлен", reply_markup=AdminMenu)
            await StateMachine.Admin.set()
