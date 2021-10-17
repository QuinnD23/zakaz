from loader import dp

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

# db_commands
from handlers.db_commands import insert_db, update_db, select_db, delete_db

# state_machine
from states.statates import StateMachine


@dp.message_handler(content_types=["photo"], state=StateMachine.PhotoTre)
async def send_photo(message: Message):
    user_id = str(message.from_user.id)
    order_id = str(await select_db("users", "user_id", "orders_count", user_id)) + "$" + user_id

    photo_mar = str(message.photo[-1].file_id)
    await update_db("orders", "id", "photo_mar", id, photo_mar)

    await message.answer("Фото маркировки стекла получено✅\n"
                         "Введите размеры трещины в см:")
    await StateMachine.DimeTre.set()
