import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_polling
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace with your actual bot token
API_TOKEN = '7837897530:AAGfJS1kQnQE-A8aEfOlzfgRu97OB2QTvi8'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

ROOMS_PER_PAGE = 10

# Set up databases
conn_ratings = sqlite3.connect("ratings.db", check_same_thread=False)
cursor_ratings = conn_ratings.cursor()

conn_hotel = sqlite3.connect('hotel_db.db', check_same_thread=False)
cursor_hotel = conn_hotel.cursor()

# Create tables if not exist
cursor_ratings.execute("""
CREATE TABLE IF NOT EXISTS user_ratings (
    user_id INTEGER PRIMARY KEY,
    rating INTEGER,
    total_rating INTEGER DEFAULT 0,
    average_rating REAL DEFAULT 0.0
)
""")
conn_ratings.commit()

cursor_hotel.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    phone TEXT,
    fio TEXT,
    email TEXT
)
""")
cursor_hotel.execute("""
CREATE TABLE IF NOT EXISTS empty_rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number INTEGER,
    room_class TEXT
)
""")
cursor_hotel.execute("""
CREATE TABLE IF NOT EXISTS booked_rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    room_number INTEGER,
    room_class TEXT,
    people_count INTEGER DEFAULT 1,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")
conn_hotel.commit()

# Function to initialize rooms
def initialize_rooms():
    room_classes = {
        "economy": 30,
        "standard": 30,
        "comfort": 15,
        "business": 15,
        "vip": 5,
    }
    room_number = 1
    for room_class, count in room_classes.items():
        for _ in range(count):
            cursor_hotel.execute(
                "INSERT INTO empty_rooms (room_number, room_class) VALUES (?, ?)",
                (room_number, room_class)
            )
            room_number += 1
    conn_hotel.commit()

cursor_hotel.execute("SELECT COUNT(*) FROM empty_rooms")
if cursor_hotel.fetchone()[0] == 0:
    initialize_rooms()

# States for user interaction
class UserStates(StatesGroup):
    send_phone = State()
    get_fio = State()
    get_email = State()

# Generate star rating keyboard
def get_star_keyboard(selected: int = 0):
    stars = ["★" if i < selected else "☆" for i in range(5)]
    buttons = [InlineKeyboardButton(stars[i], callback_data=f"rate:{i + 1}") for i in range(5)]
    return InlineKeyboardMarkup(row_width=5).add(*buttons)

# Start command handler
@dp.message_handler(commands=['start'], state="*")
async def start_func(message: types.Message):
    user_id = message.from_user.id

    cursor_ratings.execute("INSERT OR IGNORE INTO user_ratings (user_id, rating) VALUES (?, 0)", (user_id,))
    conn_ratings.commit()

    buttons = [
        KeyboardButton("Xonalarni bron qilish"),
        KeyboardButton("Mening bronlarim"),
        KeyboardButton("Reyting berish"),
        KeyboardButton("Mehmonxona haqida", web_app=WebAppInfo(url="https://hotel-uz.com/uz/booking/")),
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
    await message.answer("Assalomu Aleykum!", reply_markup=keyboard)

# Handle rating button press
@dp.message_handler(lambda message: message.text == "Reyting berish")
async def handle_rating_request(message: types.Message):
    await message.reply("Reytingni tanlang:", reply_markup=get_star_keyboard())

# Handle rating input
@dp.callback_query_handler(lambda c: c.data and c.data.startswith("rate:"))
async def rate_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    rating = int(callback_query.data.split(":")[1])

    cursor_ratings.execute("SELECT rating FROM user_ratings WHERE user_id = ?", (user_id,))
    current_rating = cursor_ratings.fetchone()

    if current_rating and current_rating[0] > 0:
        await callback_query.answer("Siz allaqachon reyting qoldirgansiz!", show_alert=True)
        return

    cursor_ratings.execute("UPDATE user_ratings SET rating = ? WHERE user_id = ?", (rating, user_id))
    conn_ratings.commit()

    cursor_ratings.execute("SELECT SUM(rating), AVG(rating) FROM user_ratings WHERE rating > 0")
    total_rating, average_rating = cursor_ratings.fetchone()

    await callback_query.message.edit_text(
        f"Siz {rating} ta yulduz tanladingiz! Reyting o‘rnatildi.\n"
        f"Umumiy reyting: {total_rating}\nO‘rtacha reyting: {average_rating:.2f}",
        reply_markup=None
    )
    await callback_query.answer()

# Display available rooms
@dp.message_handler(lambda message: message.text == "Xonalarni bron qilish")
async def empty_rooms(message: types.Message):
    cursor_hotel.execute("SELECT room_number, room_class FROM empty_rooms LIMIT ?", (ROOMS_PER_PAGE,))
    rooms = cursor_hotel.fetchall()

    if rooms:
        keyboard = InlineKeyboardMarkup()
        for room in rooms:
            keyboard.add(InlineKeyboardButton(f"Xona {room[0]} - {room[1]}", callback_data=f"book:{room[0]}"))
        await message.answer("Iltimos, bir xona tanlang:", reply_markup=keyboard)
    else:
        await message.answer("Hozirda bo‘sh xonalar mavjud emas.")

# Handle room booking
@dp.callback_query_handler(lambda c: c.data and c.data.startswith("book:"))
async def book_room_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    room_number = int(callback_query.data.split(":")[1])

    cursor_hotel.execute("SELECT room_class FROM empty_rooms WHERE room_number = ?", (room_number,))
    room = cursor_hotel.fetchone()

    if not room:
        await callback_query.answer("Bu xona allaqachon band qilingan!", show_alert=True)
        return

    cursor_hotel.execute(
        "INSERT INTO booked_rooms (user_id, room_number, room_class) VALUES (?, ?, ?)",
        (user_id, room_number, room[0])
    )
    cursor_hotel.execute("DELETE FROM empty_rooms WHERE room_number = ?", (room_number,))
    conn_hotel.commit()

    await callback_query.answer("Xona muvaffaqiyatli band qilindi!")
    await callback_query.message.edit_text(f"Xona {room_number} band qilindi.")

# Handle "Mening bronlarim"
@dp.message_handler(lambda message: message.text == "Mening bronlarim")
async def my_bookings_handler(message: types.Message):
    user_id = message.from_user.id

    cursor_hotel.execute("SELECT room_number, room_class FROM booked_rooms WHERE user_id = ?", (user_id,))
    bookings = cursor_hotel.fetchall()

    if bookings:
        booking_list = "\n".join([f"Xona {room[0]} - {room[1]}" for room in bookings])
        await message.answer(f"Sizning band qilingan xonalar:\n{booking_list}")
    else:
        await message.answer("Sizda hozircha band qilingan xonalar mavjud emas.")

if __name__ == "__main__":
    try:
        start_polling(dp, skip_updates=True)
    except Exception as e:
        logging.error(f"Botda xatolik yuz berdi: {e}")
