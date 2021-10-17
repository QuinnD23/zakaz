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

    photo_tre = str(message.photo[-1].file_id)
    await update_db("orders", "id", "photo_tre", id, photo_tre)

    await message.answer("Фото трещины получено✅\n"
                         "Отправьте фото маркировки стекла:")
    await StateMachine.PhotoMar.set()
