import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.def_menu import *
from loader import dp
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import *
from handlers.users.describe import *
from keyboards.inline.inline_buttons import *
from states.State import *

ROOMS_PER_PAGE = 10

def get_paged_rooms(rooms, page):
    start_idx = page * ROOMS_PER_PAGE
    end_idx = start_idx + ROOMS_PER_PAGE
    return rooms[start_idx:end_idx]

@dp.message_handler(commands=['start'],state="*")
async def start_func(message: types.Message):
    await message.answer(f"Assalomu Aleykum {message.from_user.first_name}!")
    await message.answer("Royxatdan otish uchun, Iltimos nomeringizni yuboring!",reply_markup=send_phone_button)
    await UserStates.send_phone.set()

@dp.message_handler(content_types=types.ContentType.CONTACT,state=UserStates.send_phone)
async def contact_func(message: types.Message):
    await message.answer("Iltimos toliq ismingizni (F.I.O) kiriting")
    await UserStates.get_fio.set()

@dp.message_handler(state=UserStates.get_fio)
async def fio_func(message: types.Message):
    fio = message.text
    print(fio)
    await message.answer("Elekntron pochtangizni yuboring!")
    await UserStates.get_email.set()


@dp.message_handler(lambda message: message.text.endswith('@gmail.com'),state=UserStates.get_email)
async def menu_func(message: types.Message, state: FSMContext):
    email = message.text
    print(email)
    await state.finish()
    buttons = [
        types.KeyboardButton("Xonalarni bron qilish"),
        types.KeyboardButton("Mehmonxona haqida",web_app=WebAppInfo(url=f"https://hotel-uz.com/uz/booking/")),
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer("Siz muafaqatli royxatdan otdingiz!")
    await message.answer("Iltimos, biror bir variantni tanlang:", reply_markup=keyboard)

@dp.message_handler(lambda message: not message.text.endswith('@gmail.com'), state=UserStates.get_email)
async def invalid_email(message: types.Message):
    await message.answer("Iltimos, faqat @gmail.com bilan tugaydigan emailni kiriting.")

@dp.message_handler(lambda message: message.text == "Xonalarni bron qilish")
async def empty_rooms(message: types.Message):
    buttons = [
        InlineKeyboardButton("💺 Ekonom", callback_data="empty_economy_0"),
        InlineKeyboardButton("🏨 Standart", callback_data="empty_standard_0"),
        InlineKeyboardButton("🌟 Komfort", callback_data="empty_comfort_0"),
        InlineKeyboardButton("💼 Biznes", callback_data="empty_business_0"),
        InlineKeyboardButton("👑 VIP", callback_data="empty_vip_0"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer("Bo'sh xonalarni ko'rish uchun xonalar sinfini tanlang:", reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith("empty_"))
async def select_empty_class(call: types.CallbackQuery):
    room_class = call.data.split("_")[1]
    page = int(call.data.split("_")[2])
    rooms = get_rooms("empty_rooms", room_class)

    current_page_rooms = get_paged_rooms(rooms, page)

    buttons = []
    for room in current_page_rooms:
        buttons.append(InlineKeyboardButton(f"🛏️ Xona {room[1]}", callback_data=f"room_{room[1]}"))

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    if page > 0:
        keyboard.add(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"empty_{room_class}_{page-1}"))

    if len(rooms) > (page + 1) * ROOMS_PER_PAGE:
        keyboard.add(InlineKeyboardButton("➡️ Keyingi", callback_data=f"empty_{room_class}_{page+1}"))

    if room_class == "economy":
        with open("images/econom-class-room.jpg", "rb") as photo:
            await call.message.answer_photo(photo, caption=description_for_eco, reply_markup=keyboard)
    elif room_class == "standard":
        with open("images/standart-class-room.jpg", "rb") as photo:
            await call.message.answer_photo(photo, caption=description_for_standart, reply_markup=keyboard)
    elif room_class == "comfort":
        with open("images/comfort-class-room.jpg", "rb") as photo:
            await call.message.answer_photo(photo, caption=description_for_comfort, reply_markup=keyboard)
    elif room_class == "business":
        with open("images/business-class-room.jpg", "rb") as photo:
            await call.message.answer_photo(photo, caption=description_for_business, reply_markup=keyboard)
    elif room_class == "vip":
        with open("images/vip-class-room.jpg", "rb") as photo:
            await call.message.answer_photo(photo, caption=description_for_vip, reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith("room_"))
async def select_room(call: types.CallbackQuery):
    room_number = int(call.data.split("_")[1])
    buttons = [
        InlineKeyboardButton("-", callback_data=f"decrease_{room_number}_2"),
        InlineKeyboardButton("2", callback_data=f"static_{room_number}_2"),
        InlineKeyboardButton("+", callback_data=f"increase_{room_number}_2"),
        InlineKeyboardButton("Bron qilish", callback_data=f"book_{room_number}_2"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    await call.message.answer(f"Xona {room_number}. Iltimos, odamlar sonini tanlang:", reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith(("increase_", "decrease_", "book_")))
async def manage_people(call: types.CallbackQuery):
    action, room_number, people = call.data.split("_")
    room_number = int(room_number)
    people = int(people)

    if action == "increase":
        people += 1
    elif action == "decrease":
        if people > 1:
            people -= 1
    elif action == "book":
        move_room_to_booked(room_number, people)
        await call.message.answer(f"Xona {room_number} {people} kishiga muvaffaqiyatli bron qilindi.")
        return

    buttons = [
        InlineKeyboardButton("-", callback_data=f"decrease_{room_number}_{people}"),
        InlineKeyboardButton(str(people), callback_data=f"static_{room_number}_{people}"),
        InlineKeyboardButton("+", callback_data=f"increase_{room_number}_{people}"),
        InlineKeyboardButton("Bron qilish", callback_data=f"book_{room_number}_{people}"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    await call.message.edit_reply_markup(reply_markup=keyboard)



