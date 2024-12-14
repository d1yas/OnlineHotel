# bot.py
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime
from database_v2 import *
from config import API_TOKEN
from keyboards.default.def_menu import menu_buttons
from keyboards.inline.inline_buttons import confirm_buttons, star_choose
from describe import *



ROOM_PRICES = {
    "economy": 10,
    "standard": 30,
    "comfort": 80,
    "business": 300,
    "vip": 800,
}

ROOM_DESCRIPTIONS = {
    "economy": description_for_eco,
    "standard": description_for_standart,
    "comfort": description_for_comfort,
    "business": description_for_business,
    "vip": description_for_vip,
}

ROOM_IMAGES = {
    "economy": "images/econom-class-room.jpg",
    "standard": "images/standart-class-room.jpg",
    "comfort": "images/comfort-class-room.jpg",
    "business": "images/business-class-room.jpg",
    "vip": "images/vip-class-room.jpg",
}


# States for booking
class BookingStates(StatesGroup):
    get_phone = State()
    get_fio = State()
    get_email = State()
    get_start_date = State()
    get_duration = State()
    get_people = State()
    confirm_booking = State()


# Initialization
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


# Start handler
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if get_user_by_id(user_id):
        await message.answer("Assalomu Aleykum! Xush kelibsiz.", reply_markup=menu_buttons)
    else:
        await message.answer(
            "Ro'yxatdan o'tish uchun telefon raqamingizni yuboring:",
            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)
            )
        )
        await BookingStates.get_phone.set()


# Phone handler
@dp.message_handler(content_types=ContentType.CONTACT, state=BookingStates.get_phone)
async def phone_handler(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone=phone_number)
    await message.answer("Iltimos to'liq ismingizni kiriting:")
    await BookingStates.get_fio.set()


# FIO handler
@dp.message_handler(state=BookingStates.get_fio)
async def fio_handler(message: types.Message, state: FSMContext):
    fio = message.text.strip()
    if len(fio.split()) < 2:
        await message.answer("❗ Iltimos, to'liq ismingizni (Ism va Familiya) kiriting.")
        return
    await state.update_data(fio=fio)
    await message.answer("Elektron pochtangizni kiriting (@gmail.com bilan tugashi kerak):")
    await BookingStates.get_email.set()


# Email handler
@dp.message_handler(lambda m: m.text.endswith("@gmail.com"), state=BookingStates.get_email)
async def email_handler(message: types.Message, state: FSMContext):
    email = message.text.strip()
    if not email.endswith("@gmail.com"):
        await message.answer("❗ Faqat @gmail.com bilan tugaydigan emailni kiriting.")
        return
    data = await state.get_data()
    add_user(user_id=message.from_user.id, phone=data['phone'], fio=data['fio'], email=email)
    await state.finish()
    await message.answer(
        "Ro'yxatdan muvaffaqiyatli o'tdingiz! Xonalarni bron qilish uchun tanlang.",
        reply_markup=menu_buttons
    )


# Invalid email handler
@dp.message_handler(lambda m: not m.text.endswith("@gmail.com"), state=BookingStates.get_email)
async def invalid_email_handler(message: types.Message):
    await message.answer("❗ Faqat @gmail.com bilan tugaydigan emailni kiriting.")


# Booking rooms
@dp.message_handler(lambda m: m.text == "Xonalarni bron qilish")
async def book_rooms(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("💺 Ekonom", callback_data="class_economy"),
        InlineKeyboardButton("🏨 Standart", callback_data="class_standard"),
        InlineKeyboardButton("🌟 Komfort", callback_data="class_comfort"),
        InlineKeyboardButton("💼 Biznes", callback_data="class_business"),
        InlineKeyboardButton("👑 VIP", callback_data="class_vip")
    )
    await message.answer("Xona turini tanlang:", reply_markup=keyboard)


# Room class selection
@dp.callback_query_handler(lambda c: c.data.startswith("class_"))
async def class_selected(call: types.CallbackQuery, state: FSMContext):
    room_class = call.data.split("_")[1]
    rooms = get_rooms("empty_rooms", room_class)
    if not rooms:
        await call.message.answer("❗ Ushbu turdagi xonalar hozir mavjud emas.")
        return
    room_number = rooms[0][1]  # First available room
    await state.update_data(room_class=room_class, room_number=room_number)

    # Display room details with image
    with open(ROOM_IMAGES[room_class], "rb") as photo:
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=ROOM_DESCRIPTIONS[room_class],
            reply_markup=None
        )

    await call.message.answer("📅 Qaysi sanadan boshlab bron qilmoqchisiz? (Format: YYYY-MM-DD)")
    await BookingStates.get_start_date.set()


# Start date input
@dp.message_handler(state=BookingStates.get_start_date)
async def start_date_handler(message: types.Message, state: FSMContext):
    date_input = message.text.strip()
    try:
        # Replace '.' or '/' with '-' to normalize the format
        normalized_date = date_input.replace(".", "-").replace("/", "-")
        start_date = datetime.strptime(normalized_date, "%Y-%m-%d")

        # Ensure the date is not in the past
        if start_date.date() < datetime.now().date():
            await message.answer("❗ Sanani kelajakdagi kunlar uchun kiriting (masalan: 2024-12-15).")
            return

        # Save to state
        await state.update_data(start_date=start_date)
        await message.answer("⏳ Necha kun bron qilmoqchisiz?")
        await BookingStates.get_duration.set()

    except ValueError:
        await message.answer(
            "❗ Sanani to'g'ri formatda kiriting: YYYY-MM-DD\n"
            "✅ Masalan: 2024-12-15"
        )


# Duration input
@dp.message_handler(state=BookingStates.get_duration)
async def duration_handler(message: types.Message, state: FSMContext):
    try:
        duration = int(message.text)
        if duration <= 0:
            await message.answer("❗ Iltimos, musbat son kiriting.")
            return

        await state.update_data(duration=duration)

        # Initialize people count to 1
        await state.update_data(people=1)

        # Initialize buttons for people selection
        people_keyboard = InlineKeyboardMarkup(row_width=4).add(
            InlineKeyboardButton("➖", callback_data="decrease_people"),
            InlineKeyboardButton("1", callback_data="static_people_1"),
            InlineKeyboardButton("➕", callback_data="increase_people"),
            InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm_people")
        )

        await message.answer("👥 Iltimos, odamlar sonini tanlang:", reply_markup=people_keyboard)
        await BookingStates.get_people.set()

    except ValueError:
        await message.answer("❗ To'g'ri raqam kiriting.")


# Manage people count
@dp.callback_query_handler(lambda call: call.data in ["increase_people", "decrease_people", "confirm_people"],
                           state=BookingStates.get_people)
async def manage_people_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    people = data.get("people", 1)

    if call.data == "increase_people":
        people += 1
    elif call.data == "decrease_people" and people > 1:
        people -= 1
    elif call.data == "confirm_people":
        room_class = data['room_class']
        duration = data['duration']
        total_cost = ROOM_PRICES[room_class] * duration

        await state.update_data(people=people, total_cost=total_cost)

        confirmation_text = (
            f"✅ Bron tafsilotlari:\n"
            f"🏨 Xona turi: {room_class.capitalize()}\n"
            f"📅 Boshlanish kuni: {data['start_date'].strftime('%Y-%m-%d')}\n"
            f"⏳ Davomiylik: {duration} kun\n"
            f"👥 Odamlar soni: {people}\n"
            f"💰 Umumiy narx: {total_cost}$"
        )

        await call.message.answer(confirmation_text, reply_markup=confirm_buttons)
        await BookingStates.confirm_booking.set()
        return

    # Update the people count and buttons
    await state.update_data(people=people)

    people_keyboard = InlineKeyboardMarkup(row_width=4).add(
        InlineKeyboardButton("➖", callback_data="decrease_people"),
        InlineKeyboardButton(str(people), callback_data=f"static_people_{people}"),
        InlineKeyboardButton("➕", callback_data="increase_people"),
        InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm_people")
    )

    await call.message.edit_reply_markup(reply_markup=people_keyboard)


# Confirm booking
@dp.callback_query_handler(lambda c: c.data == "confirm_booking", state=BookingStates.confirm_booking)
async def confirm_booking(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    data = await state.get_data()
    bookings = get_booked_rooms(user_id)
    print(bookings)

    # Move room to booked_rooms with all details
    success = move_room_to_booked_with_date(
        user_id=user_id,
        room_number=data['room_number'],
        room_class=data['room_class'],
        start_date=data['start_date'].strftime('%Y-%m-%d'),
        duration=data['duration'],
        total_cost=data['total_cost'],
        people_count=data['people']  # Odamlar sonini qo'shamiz
    )

    if success:
        await call.message.answer(
            "✅ Xona muvaffaqiyatli bron qilindi!\n"
            f"💰 Umumiy narx: {data['total_cost']}$\n"
            f"👥 Odamlar soni: {data['people']}\n"
            f"Xona raqami: {data['room_number']}\n"
            f"Xona LVL: {data['room_class']}\n"
        )
    else:
        await call.message.answer("❗ Xona bron qilishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")

    await state.finish()


# Cancel booking
@dp.callback_query_handler(lambda c: c.data == "cancel_booking", state=BookingStates.confirm_booking)
async def cancel_booking(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("❌ Bron bekor qilindi.", reply_markup=menu_buttons)
    await state.finish()


# View user's bookings
@dp.message_handler(lambda m: m.text == "Maning bronlarim")
async def get_history(message: types.Message):
    user_id = message.from_user.id
    bookings = get_booked_rooms(user_id)
    if bookings:
        response = "📋 Sizning bronlangan xonalar:\n\n"
        for idx, booking in enumerate(bookings, 1):
            response += (
                f"{idx}. Xona raqami: {booking[0]}\n"
                f"   Xona sinfi: {booking[1].capitalize()}\n"
                f"   Odamlar soni: {booking[2]}\n"
                f"   Boshlanish kuni: {booking[3]}\n"
                f"   Davomiylik: {booking[4]} kun\n"
                f"   Umumiy narx: {booking[5]}$\n\n"
            )
    else:
        response = "📋 Sizda bronlangan xonalar mavjud emas."

    await message.answer(response, reply_markup=menu_buttons)


# Rate the hotel
@dp.message_handler(lambda m: m.text == "Mexmonxonani baholash")
async def rate_handler(message: types.Message):
    user_id = message.from_user.id

    if has_rated(user_id):
        average_rating = get_average_rating()
        await message.answer(
            f"📊 Siz allaqachon baho bergansiz. Rahmat!\n"
            f"📈 Hozirgi o'rtacha baho: {round(average_rating, 2)}"
        )
    else:
        await message.answer("🌟 Iltimos, reytingingizni tanlang:", reply_markup=star_choose)


# Handle star rating
@dp.callback_query_handler(lambda call: call.data.startswith("rate_"))
async def rate_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    rating = int(call.data.split("_")[1])

    if has_rated(user_id):
        average_rating = get_average_rating()
        await call.answer(
            f"📊 Siz allaqachon baho bergansiz.\n"
            f"📈 Hozirgi o'rtacha baho: {round(average_rating, 2)}",
            show_alert=True
        )
        return

    add_rating(user_id, rating)
    average_rating = get_average_rating()

    await call.message.answer(
        f"🌟 Siz {rating} baho berdingiz.\n📈 Hozirgi o'rtacha baho: {round(average_rating, 2)}"
    )
    await call.answer()


# Error handler for invalid commands or messages
@dp.message_handler()
async def default_handler(message: types.Message):
    await message.answer("❗ Noto'g'ri buyruq. Iltimos, menyudan tanlang.", reply_markup=menu_buttons)


if __name__ == '__main__':
    start_polling(dp, skip_updates=True)
