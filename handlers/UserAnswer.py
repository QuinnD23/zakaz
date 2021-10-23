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
from kyeboards.marks import StartMenu, AnswerMenu


@dp.message_handler(state=StateMachine.UserAnswer)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    admin_id = str(await select_db("admin", "code", "admin_id", code))

    last_order = str(await select_db("users", "user_id", "last_order", user_id))
    now_order = str(await select_db("users", "user_id", "now_order", user_id))

    # ----- start
    if message.text == "/start" and last_order == now_order:
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=AnswerMenu)
        await StateMachine.UserAnswer.set()
    # -----

    if message.text == "Заказать🔥" and last_order == now_order:
        dp.bot.send_message(admin_id, f"{now_order} подтвержден✅")

        await update_db("orders", "id", "status", now_order, 1)

        await message.answer("Заказ подтвержден✅", reply_markup=StartMenu)
        await StateMachine.Start.set()

    if message.text == "Позже🕐" and last_order == now_order:
        await message.answer("Заказ перемещен в 'Мои заказы📚'", reply_markup=StartMenu)
        await StateMachine.Start.set()
