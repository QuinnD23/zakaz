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


@dp.message_handler(state=StateMachine.EditServicesCommands)
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

    if message.text == "Добавить Услугу📙":
        await message.answer("🔖Пример: Стрижка💇‍♂️\n"
                             "Введите Название Услуги:", reply_markup=BackMenu)
        await StateMachine.AddServices.set()

    if message.text == "Удалить Услугу❌":
        await message.answer("⚡️Чтобы удалить Услугу\n"
                             "Введите Номер Услуги из текущего списка:", reply_markup=BackMenu)
        await StateMachine.DeleteServices.set()


@dp.message_handler(state=StateMachine.AddServices)
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
        # Добавление услуги
        type = message.text
        try:
            await insert_db("servicesoptions", "type", type)
        except:
            pass

        # Обновление числа услуг
        services_count = int(await select_db("counters", "code", "services_count", code)) + 1
        await update_db("counters", "code", "services_count", code, services_count)

        if user_name == main_admin_name:
            await message.answer(f"📙Услуга {type} добавлена", reply_markup=MainAdminMenu)
            await StateMachine.MainAdmin.set()
        else:
            await message.answer(f"📙Услуга {type} добавлена", reply_markup=AdminMenu)
            await StateMachine.Admin.set()


@dp.message_handler(state=StateMachine.DeleteServices)
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
                # Удаление из Услуг Сотрудников
                service_num = str(await select_db("servicesoptions", "del_service_num", "service_num", del_service_num))

                worker_num = 1
                workers_count = int(await select_db("counters", "code", "workers_count", code))
                while worker_num <= workers_count:
                    try:
                        services = str(await select_db("workers", "worker_num", "services", worker_num))
                    except:
                        worker_num += 1

                    delete_service_position = services.find(service_num)
                    if delete_service_position != -1:
                        if delete_service_position - 2 < 0:
                            if delete_service_position + 1 == len(services):
                                services = "0"
                            else:
                                services = services[delete_service_position + 2:]
                        elif delete_service_position + 2 > len(services):
                            services = services[:delete_service_position - 1]
                        else:
                            services = services[:delete_service_position - 1] + services[delete_service_position + 1:]
                        await update_db("workers", "worker_num", "services", worker_num, services)

                    worker_num += 1

                # Удаление из таблицы Услуг
                await delete_db("servicesoptions", "del_service_num", del_service_num)

                if user_name == main_admin_name:
                    await message.answer(f"❌Услуга {type} удалена", reply_markup=MainAdminMenu)
                    await message.answer("‼️Внимание\n"
                                         "Услуга так же удалена из Услуг Сотрудников")
                    await StateMachine.MainAdmin.set()
                else:
                    await message.answer(f"❌Услуга {type} удалена", reply_markup=AdminMenu)
                    await message.answer("‼️Внимание\n"
                                         "Услуга так же удалена из Услуг Сотрудников")
                    await StateMachine.Admin.set()
            # check table
            else:
                await message.answer("❗️Неверный формат")
        # check_num
        else:
            await message.answer("❗️Неверный формат")
