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
        now_day = str(now.split()[0])
        now_month = str(now.split()[1])
        now_year = str(now.split()[2])
        now_hour = str(now.split()[3])
        now_min = str(now.split()[4])
        now_named_day = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime("%A"))
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
                year = str(await select_db("notifies", "id", "year", counter))
                month = str(await select_db("notifies", "id", "month", counter))
                day = str(await select_db("notifies", "id", "day", counter))
                hour = str(await select_db("notifies", "id", "hour", counter))
                min = str(await select_db("notifies", "id", "min", counter))

                if now_year == year and now_month == month and now_day == day and now_hour == hour and now_min == min:
                    counter_members = 0
                    members_count = int(await select_db("notifies", "id", "members_count", counter))
                    while counter_members < members_count:
                        id_member = str(counter) + '#' + str(counter_members)
                        try:
                            member_name = str(await select_db("notifiesmembers", "id_member", "member_name", id_member))
                        except:
                            counter_members += 1
                            continue
                        try:
                            tele_id = str(await select_db("workers", "worker_name", "tele_id", member_name))
                        except:
                            counter_members += 1
                            continue
                        if tele_id != "0":
                            await dp.bot.send_message(tele_id, text)
                        await delete_db("notifiesmembers", "id_member", id_member)
                        counter_members += 1
                    await delete_db("notifies", "id", counter)
                counter += 1
        # Проверка2
        check = True
        try:
            notifies_week_count = int(await select_db("admin", "code", "notifies_week_count", code))
        except:
            check = False
        if check:
            counter = 0
            while counter < notifies_week_count:
                try:
                    text = str(await select_db("notifiesweek", "id", "text", counter))
                except:
                    counter += 1
                    continue
                named_day = str(await select_db("notifiesweek", "id", "named_day", counter))
                hour = str(await select_db("notifiesweek", "id", "hour", counter))
                min = str(await select_db("notifiesweek", "id", "min", counter))

                if now_named_day == named_day and now_hour == hour and now_min == min:
                    counter_members = 0
                    members_count = int(await select_db("notifiesweek", "id", "members_count", counter))
                    while counter_members < members_count:
                        id_member = str(counter) + '#' + str(counter_members)
                        try:
                            member_name = str(await select_db("notifiesmembersweek", "id_member", "member_name", id_member))
                        except:
                            counter_members += 1
                            continue
                        try:
                            tele_id = str(await select_db("workers", "worker_name", "tele_id", member_name))
                        except:
                            counter_members += 1
                            continue
                        if tele_id != "0":
                            await dp.bot.send_message(tele_id, text)
                        counter_members += 1
                counter += 1
        #
        await asyncio.sleep(50)
        now = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime("%S"))
        while now != "00":
            await asyncio.sleep(1)
            now = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime("%S"))

# asyncio.run(ping())
