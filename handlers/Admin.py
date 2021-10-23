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
from kyeboards.marks import BackMenu, AdminMenu, AcceptMenu, AnswerMenu


@dp.message_handler(state=StateMachine.Admin)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
    # -----

    if message.text == "Ответить💥":
        await message.answer("💥Введите ID заказа:\n"
                             "Пример - 1$132224974", reply_markup=BackMenu)
        await StateMachine.Answer.set()


@dp.message_handler(state=StateMachine.Answer)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

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
            id = message.text
            check = True
            try:
                auto_test = await select_db("orders", "id", "auto", id)
            except:
                check = False
            if check:
                await update_db("admin", "code", "now_order", code, id)
                while id[0] != '$':
                    id = id[1:]
                id = id[1:]
                check = True
                try:
                    user_name_test = await select_db("users", "user_id", "user_name", id)
                except:
                    check = False
                if check:
                    await update_db("admin", "code", "tele_id", code, id)
                    await message.answer("💥Введите Текст сообщения:")
                    await StateMachine.AnswerText.set()
                else:
                    await message.answer("Неверный формат❌")
            else:
                await message.answer("Неверный формат❌")


@dp.message_handler(state=StateMachine.AnswerText)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

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
            text = message.text
            await update_db("admin", "code", "text", code, text)
            await message.answer(f"✍️Текст:\n"
                                 f"'{text}'\n"
                                 f"✅Вы уверены, что хотите отправить этот текст?", reply_markup=AcceptMenu)
            await StateMachine.AcceptText.set()


@dp.message_handler(state=StateMachine.AcceptText)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----
    # ----- back
    if message.text == "Отменить◀️":
        await message.answer("Возвращаю...", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    # -----

    if message.text == "Да✅":
        tele_id = await select_db("admin", "code", "tele_id", code)
        text = await select_db("admin", "code", "text", code)
        now_order = await select_db("admin", "code", "now_order", code)

        await update_db("users", "user_id", "now_order", tele_id, now_order)

        await dp.bot.send_message(tele_id, text)

        await message.answer("Ответ отправлен заказчику", reply_markup=AdminMenu)
        await StateMachine.Admin.set()

    if message.text == "Нет❌":
        await message.answer("💥Введите Текст сообщения:", reply_markup=BackMenu)
        await StateMachine.AnswerText.set()
