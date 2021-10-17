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
from kyeboards.marks import StartMenu, ChoiceAutoMenu


@dp.message_handler(Command("start"))
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)
    admin_name = str(await select_db("admin", "code", "admin_name", code))

    if user_name == admin_name:
        await update_db("admin", "code", "admin_id", code, user_id)

        await message.answer("Приветствую тебя, администратор!")
        await StateMachine.Admin.set()
    else:
        try:
            await insert_db("users", "user_id", user_id)
        except:
            pass
        await update_db("users", "user_id", "user_name", user_id, user_name)
        await update_db("users", "user_id", "autos_count", user_id, 1)
        await update_db("users", "user_id", "orders_count", user_id, 1)
        await update_db("users", "user_id", "places_count", user_id, 1)

        await message.answer(f"Приветствую, f{user_name}\n"
                             f"🛠Компания RST\n"
                             f"Ремонт и замена лобовых стекол для всех марок автомобилей")
        await message.answer("Введите ваше Имя:")
        await StateMachine.StartName.set()


@dp.message_handler(state=StateMachine.StartName)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, f{user_name}\n"
                             f"🛠Компания RST\n"
                             f"Ремонт и замена лобовых стекол для всех марок автомобилей")
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
        await message.answer(f"Приветствую, f{user_name}\n"
                             f"🛠Компания RST\n"
                             f"Ремонт и замена лобовых стекол для всех марок автомобилей")
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
        await message.answer(f"Приветствую, f{user_name}\n"
                             f"🛠Компания RST\n"
                             f"Ремонт и замена лобовых стекол для всех марок автомобилей")
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

        await message.answer("Введите VIN вашего автомобиля:")
        await StateMachine.StartVin.set()


@dp.message_handler(state=StateMachine.StartVin)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, f{user_name}\n"
                             f"🛠Компания RST\n"
                             f"Ремонт и замена лобовых стекол для всех марок автомобилей")
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
        await message.answer(f"Приветствую, f{user_name}\n"
                             f"🛠Компания RST\n"
                             f"Ремонт и замена лобовых стекол для всех марок автомобилей")
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
        await message.answer(f"Приветствую, f{user_name}\n"
                             f"🛠Компания RST\n"
                             f"Ремонт и замена лобовых стекол для всех марок автомобилей", reply_markup=StartMenu)
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
            vin = await select_db("autos", "id", "vin", id)
            await message.answer(f"Номер {counter}\n"
                                 f"🚙 Авто - {auto}\n"
                                 f"📙 VIN - {vin}")
            counter += 1

        await message.answer("⚡️Отправьте номер нужного автомобиля или добавьте новый", reply_markup=ChoiceAutoMenu)
        await StateMachine.AutoChoice.set()
