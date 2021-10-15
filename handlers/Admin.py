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
from kyeboards.marks import AdminMenu, BackMenu


@dp.message_handler(state=StateMachine.Admin)
async def mess(message: Message):

    # ----- start
    if message.text == "/start":
        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
    # -----

    if message.text == "Добавить сотрудника✅":
        await message.answer("Введите Ник Телеграм сотрудника:\n"
                             "Пример: @kquinn1", reply_markup=BackMenu)
        await StateMachine.Add.set()

    if message.text == "Удалить сотрудника❌":
        await message.answer("Список текущих сотрудников:", reply_markup=BackMenu)
        counter = 0
        delete_id = 1
        workers_count = int(await select_db("admin", "code", "workers_count", code))
        while counter < workers_count:
            try:
                worker_name = str(await select_db("workers", "id", "worker_name", counter))
            except:
                counter += 1
                continue
            await message.answer(f"{delete_id}. {worker_name}:")
            await update_db("workers", "id", "delete_id", counter, delete_id)
            counter += 1
            delete_id += 1

        await message.answer("Введите номер сотрудника, которого хотите удалить:")
        await StateMachine.Delete.set()

    if message.text == "Создать уведомление⚡️":
        await message.answer("Введите Текст уведомления:", reply_markup=BackMenu)
        await StateMachine.NotifyText.set()

    if message.text == "Редактировать уведомление✏️":
        await message.answer("⚡️Список текущих уведомлений:", reply_markup=BackMenu)
        counter = 0
        delete_id = 1
        notifies_count = int(await select_db("admin", "code", "notifies_count", code))
        while counter < notifies_count:
            try:
                text = str(await select_db("notifies", "id", "text", counter))
            except:
                counter += 1
                continue
            year = int(await select_db("notifies", "id", "year", counter))
            month = int(await select_db("notifies", "id", "month", counter))
            day = int(await select_db("notifies", "id", "day", counter))
            hour = int(await select_db("notifies", "id", "hour", counter))
            min = int(await select_db("notifies", "id", "min", counter))
            await message.answer(f"{delete_id}💥{text}\n"
                                 f"Дата - {day}.{month}.{year}\n"
                                 f"Время - {hour}:{min}")
            await update_db("notifies", "id", "delete_id", counter, delete_id)
            counter += 1
            delete_id += 1

        await message.answer("Введите номер уведомления, которое хотите изменить:")
        await StateMachine.EditChoice.set()
