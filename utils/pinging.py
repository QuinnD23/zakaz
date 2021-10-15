from aiogram import Dispatcher

import datetime

import asyncio

# config
from data.config import code

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db


async def ping(dp: Dispatcher):
    now = ""
    while now != "00":
        await asyncio.sleep(1)
        now = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime("%S"))
    while True:
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime("%d %m %Y %H %M %S")
        await dp.bot.send_message("1894744752", now)
        now_day = int(now.split()[0])
        now_month = int(now.split()[1])
        now_year = int(now.split()[2])
        now_hour = int(now.split()[3])
        now_min = int(now.split()[4])
        # Проверка
        check = True
        try:
            notifies_count = int(await select_db("admin", "code", "notifies_count", code))
        except:
            check = False
        if check:
            counter = 0
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
                await dp.bot.send_message("1894744752", f"table = {day} {month} {year} {hour} {min}")
                if now_year == year and now_month == month and now_day == day and now_hour == hour and now_min == min:
                    await dp.bot.send_message("1894744752", "yes")
                    counter_workers = 0
                    workers_count = int(await select_db("admin", "code", "workers_count", code))
                    while counter_workers < workers_count:
                        try:
                            tele_id = str(await select_db("workers", "id", "tele_id", counter_workers))
                        except:
                            counter_workers += 1
                            continue

                        await dp.bot.send_message(tele_id, text)
                        counter_workers += 1
                    await delete_db("notifies", "id", counter)

                counter += 1
        #
        await asyncio.sleep(60)

# asyncio.run(ping())
