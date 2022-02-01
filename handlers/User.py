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
from kyeboards.marks import EditUsersContactsMenu


@dp.message_handler(state=StateMachine.User)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # start
    if message.text == "/start":
        await start_command("start", user_name, user_id, dp)
    # *****

    if message.text == "Мои контакты📱":
        await message.answer("📱Список ваших Контактов:", reply_markup=EditUsersContactsMenu)
        contact_num = 1
        contacts_count = int(await select_db("counters", "code", "contacts_count", code))
        del_user_contact_id_num = 1
        while contact_num <= contacts_count:
            try:
                type = str(await select_db("contactsoptions", "contact_num", "type", contact_num))
            except:
                contact_num += 1
                continue

            # Достаем информацию по типу Контакта
            user_contact_id = contact_num + '#' + user_id

            try:
                info = str(await select_db("userscontacts", "user_contact_id", "info", user_contact_id))
            except:
                contact_num += 1
                continue

            # Вывод Информации
            await message.answer(f"{del_user_contact_id_num}. {type} - {info}")

            # del update
            del_user_contact_id = str(del_user_contact_id_num) + '#' + user_id
            await update_db("userscontacts", "user_contact_id", "del_user_contact_id", user_contact_id, del_user_contact_id)
            del_user_contact_id_num += 1

            contact_num += 1

            await StateMachine.EditUsersContactsCommands.set()

    if message.text == "Записаться🔹":
        await message.answer("🔸Выберите Услугу:", reply_markup=ReplyKeyboardRemove())

        # Кол-во заказов + 1
        orders_count = int(await select_db("users", "user_id", "orders_count", user_id)) + 1
        await update_db("users", "user_id", "orders_count", user_id, orders_count)

        # Создадим Заказ
        order_id = str(orders_count) + '#' + user_id
        try:
            await insert_db("orders", "order_id", order_id)
        except:
            pass

        # Список Услуг
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

        await message.answer("⚡️Чтобы выбрать Услугу\n"
                             "Введите Номер Услуги из списка:")

        await StateMachine.ServiceInOrder.set()
