from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import MainAdminMenu, EditAdminsMenu, EditWorkersMenu, EditServicesMenu, EditFaceMenu


@dp.message_handler(state=StateMachine.MainAdmin)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start
    if message.text == "/start" or message.text == "Отменить◀️":
        await message.answer("Приветствую тебя, ⭐️Главный Администратор!", reply_markup=MainAdminMenu)
    # *****

    if message.text == "Администраторы⭐️":
        await message.answer("💫Список текущих Администраторов:", reply_markup=EditAdminsMenu)
        admin_num = 1
        admins_count = int(await select_db("counters", "code", "admins_count", code))
        del_admin_num = 1
        while admin_num <= admins_count:
            try:
                admin_name = str(await select_db("admins", "admins_num", "admin_name", admin_num))
            except:
                admin_num += 1
                continue

            await message.answer(f"{del_admin_num}. @{admin_name}")

            # del update
            await update_db("admins", "admins_num", "del_admins_num", admin_num, del_admin_num)
            del_admin_num += 1

            admin_num += 1

        await StateMachine.EditAdminsCommands.set()

    if message.text == "Сотрудники👩‍💼":
        services_count = int(await select_db("counters", "code", "services_count", code))
        if services_count == 0:
            await message.answer("Сначала добавьте Услуги📙")
        else:
            await message.answer("👩‍💼Список текущих Сотрудников:", reply_markup=EditWorkersMenu)
            worker_num = 1
            workers_count = int(await select_db("counters", "code", "workers_count", code))
            del_worker_num = 1
            while worker_num <= workers_count:
                try:
                    worker_name = str(await select_db("workers", "worker_num", "worker_name", worker_num))
                except:
                    worker_num += 1
                    continue

                # Услуги
                services_text = ""

                services = str(await select_db("workers", "worker_num", "services", worker_num))
                service_position = 0
                while True:
                    try:
                        service_num = int(services.split()[service_position])
                    except:
                        break
                    type = str(await select_db("servicesoptions", "service_num", "type", service_num))
                    services_text += f"{type}\n"

                # Вывод Информации
                await message.answer(f"{del_worker_num}. @{worker_name}\n"
                                     f"{services_text}")

                # del update
                await update_db("workers", "worker_num", "del_worker_num", worker_num, del_worker_num)
                del_worker_num += 1

                worker_num += 1

            await StateMachine.EditWorkersCommands.set()

    if message.text == "Интерфейс Пользователя📱":
        await message.answer("Что вы хотите изменить?", reply_markup=EditFaceMenu)
        await StateMachine.EditServicesCommands.set()

    if message.text == "Услуги📙":
        await message.answer("📙Список текущих Услуг:", reply_markup=EditServicesMenu)
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

        await StateMachine.EditServicesCommands.set()
