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
from kyeboards.marks import AdsMenu, MainAdminMenu, AdminMenu


@dp.message_handler(state=StateMachine.AdsTextWait)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start
    if message.text == "/start":
        await start_command("start", user_name, user_id, dp)
    # *****

    # back
    if message.text == "Отменить◀️":
        await start_command("back", user_name, user_id, dp)
    # *****

    else:
        if user_name == main_admin_name:
            table = "mainadmin"
            id_on_table = "main_admin_id"
        else:
            table = "admins"
            id_on_table = "admin_id"
        ads_text = message.text
        await update_db(table, id_on_table, "ads_text", user_id, ads_text)
        await message.answer("⚡️Сообщение сохранено\n"
                             "Подтвердите отправку...", reply_markup=AdsMenu)

        await StateMachine.AdsMainCheck.set()


@dp.message_handler(state=StateMachine.AdsMainCheck)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start
    if message.text == "/start":
        await start_command("start", user_name, user_id, dp)
    # *****

    # back
    if message.text == "Отменить◀️":
        await start_command("back", user_name, user_id, dp)
    # *****

    if message.text == "Отправить✅":
        if user_name == main_admin_name:
            table = "mainadmin"
            id_on_table = "main_admin_id"
        else:
            table = "admins"
            id_on_table = "admin_id"
        ads_text = str(await select_db(table, id_on_table, "ads_text", user_id))
        num = 1
        err = 0
        while True:
            try:
                user_id = str(await select_db("users", "user_num", "user_id", num))
            except:
                if err >= 50:
                    break
                err += 1
                num += 1
                continue
            await dp.bot.send_message(user_id, ads_text)
            num += 1

        await message.answer("🌀Реклама отправляется...\n"
                             "Дождитесь завершения отправки", reply_markup=ReplyKeyboardRemove())

        if user_name == main_admin_name:
            await message.answer("💎Реклама успешно отправлена", reply_markup=MainAdminMenu)
            await StateMachine.MainAdmin.set()
        else:
            await message.answer("💎Реклама успешно отправлена", reply_markup=AdminMenu)
            await StateMachine.Admin.set()
