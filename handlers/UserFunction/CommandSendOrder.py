from aiogram import Dispatcher

# config
from data.config import code, channel_id

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db


async def send_order(user_id, dp: Dispatcher):
    user_name = str(await select_db("users", "user_id", "user_name", user_id))

    # Контакты Пользователя
    contacts_text = ""

    contact_num = 1
    contacts_count = int(await select_db("counters", "code", "contacts_count", code))
    while contact_num <= contacts_count:
        try:
            type = str(await select_db("contactsoptions", "contact_num", "type", contact_num))
        except:
            contact_num += 1
            continue

        user_contact_id = str(contact_num) + '#' + user_id
        info = str(await select_db("userscontacts", "user_contact_id", "info", user_contact_id))

        contacts_text += f"🔹{type}: {info}\n"

        contact_num += 1

    # Информация о Заказе
    orders_count = str(await select_db("users", "user_id", "orders_count", user_id))
    order_id = orders_count + '#' + user_id

    service = str(await select_db("orders", "order_id", "service", order_id))
    date = str(await select_db("orders", "order_id", "date", order_id))
    time = str(await select_db("orders", "order_id", "time", order_id))
    worker = str(await select_db("orders", "order_id", "worker", order_id))

    await dp.bot.send_message(channel_id, f"❗️Заказ\n"
                                          f"🔷Имя Пользователя: @{user_name}\n"
                                          f"{contacts_text}\n"
                                          f"\n"
                                          f"📙Услуга: {service}\n"
                                          f"🗓Дата: {date}\n"
                                          f"🕐Время: {time}\n"
                                          f"👩‍💼Мастер: {worker}")
