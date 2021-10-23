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
from kyeboards.marks import StartMenu, ChoiceAutoMenu, AdminMenu, MyOrdersMenu


@dp.message_handler(Command("start"))
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    admin_name = str(await select_db("admin", "code", "admin_name", code))

    if user_name == admin_name:
        await update_db("admin", "code", "admin_id", code, user_id)

        await message.answer("Приветствую тебя, администратор!", reply_markup=AdminMenu)
        await StateMachine.Admin.set()
    else:
        users_count = int(await select_db("admin", "code", "users_count", code))
        users_count += 1
        await update_db("admin", "code", "users_count", code, users_count)

        try:
            await insert_db("users", "user_id", user_id)
        except:
            pass
        await update_db("users", "user_id", "user_name", user_id, user_name)
        await update_db("users", "user_id", "autos_count", user_id, 1)
        await update_db("users", "user_id", "orders_count", user_id, 1)
        await update_db("users", "user_id", "places_count", user_id, 1)

        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией")
        await message.answer("Введите ваше Имя:")
        await StateMachine.StartName.set()


@dp.message_handler(state=StateMachine.StartName)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией")
        await message.answer("Введите ваше Имя:")
        await StateMachine.StartName.set()
    # -----
    else:
        name = message.text
        await update_db("users", "user_id", "name", user_id, name)

        await message.answer("Введите ваш Контактный номер:")
        await StateMachine.StartNumber.set()


@dp.message_handler(state=StateMachine.StartNumber)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией")
        await message.answer("Введите ваше Имя:")
        await StateMachine.StartName.set()
    # -----
    else:
        number = message.text
        await update_db("users", "user_id", "number", user_id, number)

        await message.answer("Введите Марку вашего авто:")
        await StateMachine.StartAuto.set()


@dp.message_handler(state=StateMachine.StartAuto)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией")
        await message.answer("Введите ваше Имя:")
        await StateMachine.StartName.set()
    # -----
    else:
        id = str(await select_db("users", "user_id", "autos_count", user_id)) + "$" + user_id
        auto = message.text
        try:
            await insert_db("autos", "id", id)
        except:
            pass
        await update_db("autos", "id", "auto", id, auto)

        # await message.answer("Введите VIN вашего автомобиля:")
        # await StateMachine.StartVin.set()
        await message.answer("Введите Год Выпуска вашего автомобиля:")
        await StateMachine.StartYear.set()


@dp.message_handler(state=StateMachine.StartYear)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией")
        await message.answer("Введите ваше Имя:")
        await StateMachine.StartName.set()
    # -----
    else:
        id = str(await select_db("users", "user_id", "autos_count", user_id)) + "$" + user_id
        year = message.text
        await update_db("autos", "id", "year", id, year)

        autos_count = int(await select_db("users", "user_id", "autos_count", user_id)) + 1
        await update_db("users", "user_id", "autos_count", user_id, autos_count)

        await message.answer("Введите ваш Район:")
        await StateMachine.StartPlace.set()


@dp.message_handler(state=StateMachine.StartVin)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией")
        await message.answer("Введите ваше Имя:")
        await StateMachine.StartName.set()
    # -----
    else:
        id = str(await select_db("users", "user_id", "autos_count", user_id)) + "$" + user_id
        vin = message.text
        await update_db("autos", "id", "vin", id, vin)

        autos_count = int(await select_db("users", "user_id", "autos_count", user_id)) + 1
        await update_db("users", "user_id", "autos_count", user_id, autos_count)

        await message.answer("Введите ваш Район:")
        await StateMachine.StartPlace.set()


@dp.message_handler(state=StateMachine.StartPlace)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией")
        await message.answer("Введите ваше Имя:")
        await StateMachine.StartName.set()
    # -----
    else:
        id = str(await select_db("users", "user_id", "places_count", user_id)) + "$" + user_id
        place = message.text
        try:
            await insert_db("places", "id", id)
        except:
            pass
        await update_db("places", "id", "place", id, place)

        places_count = int(await select_db("users", "user_id", "places_count", user_id)) + 1
        await update_db("users", "user_id", "places_count", user_id, places_count)

        await message.answer("Регистрация пройдена успешно✅", reply_markup=StartMenu)
        await StateMachine.Start.set()


@dp.message_handler(state=StateMachine.Start)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=StartMenu)
        await message.answer("Введите ваше Имя:")
    # -----

    if message.text == "Новый заказ🛠":
        id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id
        try:
            await insert_db("orders", "id", id)
        except:
            pass

        await message.answer("Выберите автомобиль:", reply_markup=ReplyKeyboardRemove())

        counter = 1
        autos_count = int(await select_db("users", "user_id", "autos_count", user_id))
        while counter < autos_count:
            id = str(counter) + "$" + user_id
            auto = await select_db("autos", "id", "auto", id)
            year = await select_db("autos", "id", "year", id)
            await message.answer(f"Номер {counter}\n"
                                 f"🚙 Авто - {auto}\n"
                                 f"📙 Год выпуска - {year}")
            counter += 1

        await message.answer("⚡️Отправьте номер нужного автомобиля или добавьте новый", reply_markup=ChoiceAutoMenu)
        await StateMachine.AutoChoice.set()

    if message.text == "Мои заказы📚":
        orders_count = await select_db("users", "user_id", "orders_count", user_id)
        counter = 1
        delete_id = 1
        while counter < orders_count:
            id = str(counter) + '$' + user_id
            try:
                status = int(await select_db("orders", "id", "status", id))
            except:
                counter += 1
                continue
            if status == 0:
                auto = str(await select_db("orders", "id", "auto", id))
                year = str(await select_db("orders", "id", "year", id))
                dime_tre = str(await select_db("orders", "id", "dime_tre", id))
                srok_tre = str(await select_db("orders", "id", "srok_tre", id))
                place = str(await select_db("orders", "id", "place", id))
                await message.answer(f"{delete_id}💥Заказ"
                                     f"🚙 Авто: {auto}\n"
                                     f"📙 Год выпуска: {year}\n"
                                     f"🏝 Район: {place}\n"
                                     f"🔹 Размер трещины: {dime_tre}см\n"
                                     f"🔹 Срок: {srok_tre}")
                await update_db("orders", "id", "delete_id", id, delete_id)
                delete_id += 1
            counter += 1
        if delete_id == 1:
            await message.answer("У вас нет непринятых заказов")
        else:
            await message.answer("Если вы хотите подтвердить заказ, нажмите 'Подтвердить✅'", reply_markup=MyOrdersMenu)
            await StateMachine.AcceptMyOrders.set()

    if message.text == "Информация📖":
        await message.answer("💥Информация")
