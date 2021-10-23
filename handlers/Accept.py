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
from kyeboards.marks import StartMenu, BackMenu


@dp.message_handler(state=StateMachine.AcceptMyOrders)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----
    # ----- back
    if message.text == "Отменить◀️":
        await message.answer("Возвращаю...", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----

    if message.text == "Подтвердить✅":
        await message.answer("✅Введите номер заказа, который хотите подтвердить:", reply_markup=BackMenu)
        await StateMachine.NumMyOrders.set()


@dp.message_handler(state=StateMachine.NumMyOrders)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    admin_id = str(await select_db("admin", "code", "admin_id", code))

    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----
    else:
        # ----- back
        if message.text == "Отменить◀️":
            await message.answer("Возвращаю...", reply_markup=StartMenu)
            await StateMachine.Start.set()
        # -----
        else:
            delete_id = message.text
            check = True
            try:
                delete_id = int(delete_id)
            except:
                check = False

            if check:
                check = True
                try:
                    now_order = await select_db("orders", "delete_id", "id", delete_id)
                except:
                    check = False

                if check:
                    await dp.bot.send_message(admin_id, f"{now_order} подтвержден✅")

                    await update_db("orders", "id", "status", now_order, 1)
                    await update_db("orders", "id", "delete_id", now_order, -1)

                    await message.answer("Заказ подтвержден✅", reply_markup=StartMenu)
                    await StateMachine.Start.set()
                else:
                    await message.answer("Неверный формат❌")
            else:
                await message.answer("Неверный формат❌")