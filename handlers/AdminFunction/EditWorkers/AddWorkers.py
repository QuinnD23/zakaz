from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import MainAdminMenu, StopMenu, AdminMenu


@dp.message_handler(state=StateMachine.AddWorkers)
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
        # Добавление сотрудника
        worker_name = message.text
        worker_name = worker_name[1:]
        try:
            await insert_db("workers", "worker_name", worker_name)
        except:
            pass

        # Укажем текущего работника, чтобы добавить ему услуги
        if user_name == main_admin_name:
            table = "mainadmin"
            id_on_table = "main_admin_id"
        else:
            table = "admins"
            id_on_table = "admin_id"
        await update_db(table, id_on_table, "add_worker_name", user_id, worker_name)

        # Обновление числа сотрудников
        workers_count = int(await select_db("counters", "code", "workers_count", code)) + 1
        await update_db("counters", "code", "workers_count", code, workers_count)

        await message.answer(f"👩‍💼Сотрудник @{worker_name} добавлен")

        # Спсисок Текущих услуг
        await message.answer("📙Список текущих Услуг:")
        service_num = 1
        services_count = int(await select_db("counters", "code", "services_count", code))
        del_service_num = 1
        while service_num <= services_count:
            try:
                type = str(await select_db("servicesoptions", "service_num", "type", service_num))
            except:
                service_num += 1
                continue

            await message.answer(f"{del_service_num}. {type}")

            # del update
            await update_db("servicesoptions", "service_num", "del_service_num", service_num, del_service_num)
            del_service_num += 1

            service_num += 1

        await message.answer("⚡️Чтобы установить Услугу Сотруднику\n"
                             "Введите Номер Услуги из текущего списка:", reply_markup=StopMenu)
        await StateMachine.AddWorkersServices.set()


@dp.message_handler(state=StateMachine.AddWorkersServices)
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
        if message.text == "Стоп⛔️":
            # Сортировка services
            if user_name == main_admin_name:
                table = "mainadmin"
                id_on_table = "main_admin_id"
            else:
                table = "admins"
                id_on_table = "admin_id"
            add_worker_name = str(await select_db(table, id_on_table, "add_worker_name", user_id))
            services = str(await select_db("workers", "worker_name", "services", add_worker_name))
            services_array = []
            services_position = 0
            while True:
                try:
                    services_array_element = str(services.split()[services_position])
                except:
                    break
                services_array.append(services_array_element)
                services_position += 1
            services_array = sorted(services_array)
            services = ""
            for i in range(0, len(services_array)):
                services += services_array[i]
            await update_db("workers", "worker_name", "services", add_worker_name, services)

            if user_name == main_admin_name:
                await message.answer("📙Все услуги добавлены", reply_markup=MainAdminMenu)
                await StateMachine.MainAdmin.set()
            else:
                await message.answer("📙Все услуги добавлены", reply_markup=AdminMenu)
                await StateMachine.Admin.set()
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
                # Добавление сервиса Сотруднику
                if user_name == main_admin_name:
                    table = "mainadmin"
                    id_on_table = "main_admin_id"
                else:
                    table = "admins"
                    id_on_table = "admin_id"
                add_worker_name = str(await select_db(table, id_on_table, "add_worker_name", user_id))
                service_num = str(await select_db("servicesoptions", "del_service_num", "service_num", del_service_num))
                services = str(await select_db("workers", "worker_name", "services", add_worker_name)) + " " + service_num
                await update_db("workers", "worker_name", "services", add_worker_name, services)

                await message.answer(f"📙Услуга {type} добавлена")
            # check table
            else:
                await message.answer("❗️Неверный формат")
        # check_num
        else:
            await message.answer("❗️Неверный формат")
