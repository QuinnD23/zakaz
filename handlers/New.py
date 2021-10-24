from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine

# marks
from kyeboards.marks import StartMenu, ChoicePlaceMenu, BonusMenu, AnswerMenu


@dp.message_handler(state=StateMachine.AutoChoice)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----
    else:
        # ----- back
        if message.text == "Отменить◀️":
            await message.answer("Возвращаю...", reply_markup=StartMenu)
            await StateMachine.Start.set()
        # -----
        else:
            if message.text == "Добавить авто➕":
                await message.answer("Введите Марку вашего авто:", reply_markup=ReplyKeyboardRemove())
                await StateMachine.AddAuto.set()
            else:
                check = True
                try:
                    num = int(message.text)
                except:
                    check = False

                if check:
                    auto_id = str(num) + "$" + user_id
                    check = True
                    try:
                        auto = await select_db("autos", "id", "auto", auto_id)
                    except:
                        check = False

                    if check:
                        year = await select_db("autos", "id", "year", auto_id)
                        order_id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id
                        await update_db("orders", "id", "auto", order_id, auto)
                        await update_db("orders", "id", "year", order_id, year)

                        await message.answer("Автомобиль выбран✅\n"
                                             "Загрузите фотографию повреждения:", reply_markup=ReplyKeyboardRemove())
                        await StateMachine.PhotoTre.set()
                    else:
                        await message.answer("Неверный формат❌")
                else:
                    await message.answer("Неверный формат❌")


@dp.message_handler(state=StateMachine.AddAuto)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----
    else:
        id = str(await select_db("users", "user_id", "autos_count", user_id)) + "$" + user_id
        auto = message.text
        try:
            await insert_db("autos", "id", id)
        except:
            pass
        await update_db("autos", "id", "auto", id, auto)

        order_id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id
        await update_db("orders", "id", "auto", order_id, auto)

        # await message.answer("Введите VIN вашего автомобиля:")
        # await StateMachine.AddVin.set()
        await message.answer("Введите Год Выпуска вашего автомобиля:")
        await StateMachine.AddYear.set()


@dp.message_handler(state=StateMachine.AddYear)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----
    else:
        id = str(await select_db("users", "user_id", "autos_count", user_id)) + "$" + user_id
        year = message.text
        await update_db("autos", "id", "year", id, year)

        autos_count = int(await select_db("users", "user_id", "autos_count", user_id)) + 1
        await update_db("users", "user_id", "autos_count", user_id, autos_count)

        order_id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id
        await update_db("orders", "id", "year", order_id, year)

        await message.answer("Автомобиль выбран✅\n"
                             "Загрузите фотографию повреждения:", reply_markup=ReplyKeyboardRemove())
        await StateMachine.PhotoTre.set()


@dp.message_handler(state=StateMachine.AddVin)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----
    else:
        id = str(await select_db("users", "user_id", "autos_count", user_id)) + "$" + user_id
        vin = message.text
        await update_db("autos", "id", "vin", id, vin)

        autos_count = int(await select_db("users", "user_id", "autos_count", user_id)) + 1
        await update_db("users", "user_id", "autos_count", user_id, autos_count)

        order_id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id
        await update_db("orders", "id", "vin", order_id, vin)

        await message.answer("Автомобиль выбран✅\n"
                             "Загрузите фотографию повреждения:", reply_markup=ReplyKeyboardRemove())
        await StateMachine.PhotoTre.set()


@dp.message_handler(state=StateMachine.DimeTre)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----
    else:
        check = True
        try:
            dime_tre = int(message.text)
        except:
            check = False

        if check:
            order_id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id
            await update_db("orders", "id", "dime_tre", order_id, dime_tre)

            await message.answer("Данные о размере получены✅\n"
                                 "Введите когда была получена трещина:")
            await StateMachine.SrokTre.set()
        else:
            await message.answer("Неверный формат❌")


@dp.message_handler(state=StateMachine.SrokTre)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----
    else:
        order_id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id
        srok_tre = message.text
        await update_db("orders", "id", "srok_tre", order_id, srok_tre)

        await message.answer("Данные о сроке получены✅\n"
                             "Выберите район:", reply_markup=ChoicePlaceMenu)

        counter = 1
        places_count = int(await select_db("users", "user_id", "places_count", user_id))
        while counter < places_count:
            id = str(counter) + "$" + user_id
            place = await select_db("places", "id", "place", id)

            await message.answer(f"Номер {counter}\n"
                                 f"🏝 Район - {place}")
            counter += 1

        await message.answer("⚡️Отправьте номер нужного района или добавьте новый")
        await StateMachine.PlaceChoice.set()


@dp.message_handler(state=StateMachine.PlaceChoice)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----
    else:
        if message.text == "Добавить район➕":
            await message.answer("Введите ваш Район:", reply_markup=ReplyKeyboardRemove())
            await StateMachine.AddPlace.set()
        else:
            check = True
            try:
                num = int(message.text)
            except:
                check = False

            if check:
                place_id = str(num) + "$" + user_id
                check = True
                try:
                    place = await select_db("places", "id", "place", place_id)
                except:
                    check = False

                if check:
                    order_id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id
                    await update_db("orders", "id", "place", order_id, place)

                    await message.answer("Район выбран✅\n"
                                         "Введите код скидки, если имеется:", reply_markup=BonusMenu)
                    await StateMachine.Bonus.set()
                else:
                    await message.answer("Неверный формат❌")
            else:
                await message.answer("Неверный формат❌")


@dp.message_handler(state=StateMachine.AddPlace)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=StartMenu)
        await StateMachine.Start.set()
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

        order_id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id
        await update_db("orders", "id", "place", order_id, place)

        await message.answer("Район выбран✅\n"
                             "Введите код скидки, если имеется:", reply_markup=BonusMenu)
        await StateMachine.Bonus.set()


@dp.message_handler(state=StateMachine.Bonus)
async def mess(message: Message):
    user_name = str(message.from_user.username)
    user_id = str(message.from_user.id)

    # ----- start
    if message.text == "/start":
        await message.answer(f"Приветствую, {user_name}")
        await message.answer("🛠Компания RST\n"
                             "Производит ремонт и замену лобовых стекол на все марки автомобилей\n"
                             "⚡️Качественно, быстро и с гарантией", reply_markup=StartMenu)
        await StateMachine.Start.set()
    # -----
    else:

        if message.text == "Нет скидки❌":
            bonus = "Нет бонуса"
        else:
            bonus = message.text
            bonus_from_table = str(await select_db("users", "user_id", "bonus", user_id))
            if bonus == bonus_from_table:
                my_bonus_counter = int(await select_db("users", "user_id", "my_bonus_counter", user_id))
                if my_bonus_counter == 0:
                    await message.answer("Бонус засчитан🔮")
                    bonus = "Бонус засчитан"
                    my_bonus_counter += 1
                    await update_db("users", "user_id", "my_bonus_counter", user_id, my_bonus_counter)
            else:
                users_count = int(await select_db("admin", "code", "users_count", code))
                counter = 1
                while counter <= users_count:
                    try:
                        bonus_from_table = str(await select_db("users", "user_num", "bonus", counter))
                    except:
                        counter += 1
                        continue
                    if bonus == bonus_from_table:
                        friend_bonus_counter = int(await select_db("users", "user_id", "friend_bonus_counter", user_id))
                        if friend_bonus_counter == 0:
                            await message.answer("Бонус засчитан🔮")
                            bonus = "Бонус засчитан"
                            friend_bonus_counter += 1
                            await update_db("users", "user_id", "friend_bonus_counter", user_id, friend_bonus_counter)
                            break
                    counter += 1

        order_id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id
        await update_db("orders", "id", "bonus", order_id, bonus)

        admin_id = str(await select_db("admin", "code", "admin_id", code))

        name = str(await select_db("users", "user_id", "name", user_id))
        number = str(await select_db("users", "user_id", "number", user_id))

        auto = str(await select_db("orders", "id", "auto", order_id))
        year = str(await select_db("orders", "id", "year", order_id))
        dime_tre = str(await select_db("orders", "id", "dime_tre", order_id))
        srok_tre = str(await select_db("orders", "id", "srok_tre", order_id))
        place = str(await select_db("orders", "id", "place", order_id))

        photo_tre = str(await select_db("orders", "id", "photo_tre", order_id))
        photo_mar = str(await select_db("orders", "id", "photo_mar", order_id))

        await dp.bot.send_message(admin_id, f"❗️ Новый заказ №{order_id}\n"
                                            f"\n"
                                            f"🔹 Телеграм: @{user_name}\n"
                                            f"🔹 Имя: {name}\n"
                                            f"📞 Телефон: {number}\n"
                                            f"🚙 Авто: {auto}\n"
                                            f"📙 Год выпуска: {year}\n"
                                            f"🏝 Район: {place}\n"
                                            f"🔹 Размер: {dime_tre}см\n"
                                            f"🔹 Срок: {srok_tre}\n"
                                            f"🔮 Бонус: {bonus}")

        await dp.bot.send_photo(admin_id, photo_tre, caption=f"Фото повреждения №{order_id}")
        await dp.bot.send_photo(admin_id, photo_mar, caption=f"Фото маркировки №{order_id}")

        orders_count = int(await select_db("users", "user_id", "orders_count", user_id)) + 1
        await update_db("users", "user_id", "orders_count", user_id, orders_count)

        await update_db("users", "user_id", "last_order", user_id, order_id)

        await message.answer("Закакз успешно создан🛠\n"
                             "Ожидайте ответа", reply_markup=AnswerMenu)
        await StateMachine.UserAnswer.set()
