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
from kyeboards.marks import MainAdminMenu, BackMenu, AdminMenu


@dp.message_handler(state=StateMachine.EditWorkersCommands)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    main_admin_name = str(await select_db("mainadmin", "code", "main_admin_name", code))

    # start and back
    if message.text == "/start" or message.text == "Отменить◀️":
        await start_command(user_name, user_id, dp)
    # *****

    if message.text == "Добавить Сотрудника👩‍💼":
        await message.answer("🔖Пример: @kquinn1\n"
                             "Введите Telegram Ник Сотрудника:", reply_markup=BackMenu)
        await StateMachine.AddWorkers.set()

    if message.text == "Удалить Сотрудника❌":
        await message.answer("⚡️Чтобы удалить Сотрудника\n"
                             "Введите Номер Сотрудника из текущего списка:", reply_markup=BackMenu)
        await StateMachine.DeleteWorkers.set()

    if message.text == "Редактировать Услуги📙":
        await message.answer("⚡️Чтобы изменить Услуги Сотрудника\n"
                             "Введите Номер Сотрудника из текущего списка:", reply_markup=BackMenu)
        await StateMachine.WaitWorkerForEditServices.set()
