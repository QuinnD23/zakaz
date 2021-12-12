from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# start_command
from handlers.CommandStart import start_command

# send_commands
from handlers.UserFunction.CommandSendOrder import send_order

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import UserMenu


@dp.message_handler(state=StateMachine.ServiceInOrder)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start and back
    if message.text == "/start":
        await start_command(user_name, user_id, dp)
    # *****

    else:
        # Проверка на число
        check_num = True
        del_service_num = message.text
        try:
            del_service_num = int(del_service_num)
        except:
            check_num = False

        if check_num:
            # Проверка на существования
            check_table = True
            try:
                type = str(await select_db("servicesoptions", "del_service_num", "type", del_service_num))
            except:
                check_table = False

            if check_table:
                # Запись Услуги в Orders
                orders_count = str(await select_db("users", "user_id", "orders_count", user_id))
                order_id = orders_count + '#' + user_id
                await update_db("orders", "order_id", "service", order_id, type)

                # Информация о времени работы
                work_time_text = str(await select_db("options", "code", "work_time_text", code))
                await message.answer(f"{work_time_text}")

                await message.answer("🔖Пример: 17.11.2021\n"
                                     "🗓Напишите желаемую Дату:")

                await StateMachine.DateInOrder.set()
            # check table
            else:
                await message.answer("❗️Неверный формат")
        # check_num
        else:
            await message.answer("❗️Неверный формат")


@dp.message_handler(state=StateMachine.DateInOrder)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start and back
    if message.text == "/start":
        await start_command(user_name, user_id, dp)
    # *****

    else:
        # Запись Даты в Orders
        date = message.text

        orders_count = str(await select_db("users", "user_id", "orders_count", user_id))
        order_id = orders_count + '#' + user_id

        await update_db("orders", "order_id", "date", order_id, date)

        await message.answer("🔖Пример: 15:00\n"
                             "🕐Напишите желаемое Время:")

        await StateMachine.TimeInOrder.set()


@dp.message_handler(state=StateMachine.TimeInOrder)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start and back
    if message.text == "/start":
        await start_command(user_name, user_id, dp)
    # *****

    else:
        # Запись Времени в Orders
        time = message.text

        orders_count = str(await select_db("users", "user_id", "orders_count", user_id))
        order_id = orders_count + '#' + user_id

        await update_db("orders", "order_id", "time", order_id, time)

        await message.answer("👩‍💼Выберите желаемого Мастера:")

        # Список Мастеров
        worker_num = 1
        workers_count = int(await select_db("counters", "code", "workers_count", code))
        del_worker_num = 1
        while worker_num <= workers_count:
            try:
                worker_name = str(await select_db("workers", "worker_num", "worker_name", worker_num))
            except:
                worker_num += 1
                continue

            # Вывод Информации
            await message.answer(f"{del_worker_num}. {worker_name}")

            # del update
            await update_db("workers", "worker_num", "del_worker_num", worker_num, del_worker_num)
            del_worker_num += 1

            worker_num += 1

        await message.answer(f"{del_worker_num}. Мастер не важен")
        # Запись номера "Мастер не важен"
        await update_db("orders", "order_id", "del_no_worker", order_id, del_worker_num)

        await message.answer("⚡️Чтобы выбрать Мастера\n"
                             "Введите Номер Мастера из списка:")

        await StateMachine.WorkerInOrder.set()


@dp.message_handler(state=StateMachine.WorkerInOrder)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start and back
    if message.text == "/start":
        await start_command(user_name, user_id, dp)
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

            # Проверка "Мастер не важен"
            orders_count = str(await select_db("users", "user_id", "orders_count", user_id))
            order_id = orders_count + '#' + user_id
            del_no_worker = str(await select_db("orders", "order_id", "del_no_worker", order_id))
            if del_worker_num == del_no_worker:
                check_table = True
                worker_name = "Мастер не важен"

            if check_table:
                # Запись Мастера в Orders
                orders_count = str(await select_db("users", "user_id", "orders_count", user_id))
                order_id = orders_count + '#' + user_id
                await update_db("orders", "order_id", "worker", order_id, worker_name)

                # Отправка Заказа в Группу Администраторов
                await send_order(user_id, dp)

                # Удаление Order


                # Завершение
                end_text = str(await select_db("options", "code", "end_text", code))
                await message.answer(f"{end_text}", reply_markup=UserMenu)

                await StateMachine.User.set()
            # check table
            else:
                await message.answer("❗️Неверный формат")
        # check_num
        else:
            await message.answer("❗️Неверный формат")
