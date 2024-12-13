from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_polling
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from database import *
from config import *
# Set up logging
logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# State management
class UserStates(StatesGroup):
    send_phone = State()
    get_fio = State()
    get_email = State()

# Main keyboard
def get_main_keyboard():
    buttons = [
        KeyboardButton("Xonalarni bron qilish"),
        KeyboardButton("Mening bronlarim"),
        KeyboardButton("Mehmonxona haqida", web_app=WebAppInfo(url="https://hotel-uz.com/uz/booking/")),
    ]
    return ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

# Start command
@dp.message_handler(commands=['start'], state="*")
async def start_func(message: types.Message):
    user = get_user_by_id(message.from_user.id)
    if user:
        await message.answer(f"Assalomu Aleykum {user['fio']}!", reply_markup=get_main_keyboard())
    else:
        await message.answer("Royxatdan o'tish uchun nomeringizni yuboring!", 
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                 KeyboardButton("Telefon raqamni yuborish", request_contact=True)))
        await UserStates.send_phone.set()

# Registration steps
@dp.message_handler(content_types=ContentType.CONTACT, state=UserStates.send_phone)
async def contact_func(message: types.Message, state):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Ismingizni kiriting:")
    await UserStates.get_fio.set()

@dp.message_handler(state=UserStates.get_fio)
async def fio_func(message: types.Message, state):
    await state.update_data(fio=message.text)
    await message.answer("Elektron pochtangizni kiriting:")
    await UserStates.get_email.set()

@dp.message_handler(lambda msg: msg.text.endswith("@gmail.com"), state=UserStates.get_email)
async def email_func(message: types.Message, state):
    data = await state.get_data()
    add_user(message.from_user.id, data['phone'], data['fio'], message.text)
    await state.finish()
    await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz!", reply_markup=get_main_keyboard())

# Room booking
@dp.message_handler(lambda msg: msg.text == "Xonalarni bron qilish")
async def show_empty_rooms(message: types.Message):
    buttons = [
        InlineKeyboardButton("💺 Ekonom", callback_data="empty_economy"),
        InlineKeyboardButton("🌟 Komfort", callback_data="empty_comfort"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=2).add(*buttons)
    await message.answer("Xona turini tanlang:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("empty_"))
async def show_rooms(call: types.CallbackQuery):
    room_class = call.data.split("_")[1]
    rooms = get_rooms("empty_rooms", room_class)
    if not rooms:
        await call.message.answer("Bu turdagi xonalar mavjud emas!")
    else:
        buttons = [InlineKeyboardButton(f"🛏️ Xona {r[1]}", callback_data=f"book_{r[1]}") for r in rooms[:5]]
        keyboard = InlineKeyboardMarkup().add(*buttons)
        await call.message.answer(f"{room_class} turidagi xonalar:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("book_"))
async def book_room(call: types.CallbackQuery):
    room_number = int(call.data.split("_")[1])
    move_room_to_booked(call.from_user.id, room_number, 1)
    await call.message.answer(f"Xona {room_number} muvaffaqiyatli bron qilindi!")

if __name__ == "__main__":
    start_polling(dp, skip_updates=True)
