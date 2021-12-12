from data.config import code

from handlers.db_commands import insert_db, update_db


async def kquinn1_admin():
    try:
        await insert_db("mainadmin", "code", code)
    except:
        pass

    await update_db("mainadmin", "code", "main_admin_name", code, "kquinn1")
