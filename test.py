# import sqlite3
# from aiogram.dispatcher import FSMContext
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.types import WebAppInfo
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.utils.executor import start_polling
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from database import *
# from describe import *
# from config import *
# from aiogram.types import Message
# from state import *
# from keyboards.default.def_menu import *
# from keyboards.inline.inline_buttons import *
# from aiogram.dispatcher.filters import Command


# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot, storage=MemoryStorage())
# dp.middleware.setup(LoggingMiddleware())

# ROOMS_PER_PAGE = 10


# def get_paged_rooms(rooms, page):
#     start_idx = page * ROOMS_PER_PAGE
#     end_idx = start_idx + ROOMS_PER_PAGE
#     return rooms[start_idx:end_idx]


# @dp.message_handler(commands=['start'])
# async def start_func(message: types.Message):
#     user_id = message.from_user.id
#     user = get_user_by_id(user_id)

#     if user:
#         await message.answer(f"Assalomu Aleykum {user['fio']}!", reply_markup=menu_buttons)
#     else:
#         await message.answer("Assalomu Aleykum!")
#         await message.answer("Royxatdan otish uchun, Iltimos nomeringizni yuboring!",
#                              reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
#                                  KeyboardButton("Telefon raqamni yuborish",request_contact=True, one_time_keyboard=True)))
#         await UserStates.send_phone.set()


# @dp.message_handler(content_types=ContentType.CONTACT, state=UserStates.send_phone)
# async def contact_func(message: types.Message, state: FSMContext):
#     phone = message.contact.phone_number
#     await state.update_data(phone=phone)
#     await message.answer("Iltimos toliq ismingizni (F.I.O) kiriting")
#     await UserStates.get_fio.set()


# @dp.message_handler(state=UserStates.get_fio)
# async def fio_func(message: types.Message, state: FSMContext):
#     fio = message.text
#     await state.update_data(fio=fio)
#     await message.answer("Elektron pochtangizni yuboring!")
#     await UserStates.get_email.set()


# @dp.message_handler(lambda message: message.text.endswith('@gmail.com'), state=UserStates.get_email)
# async def menu_func(message: types.Message, state: FSMContext):
#     email = message.text
#     data = await state.get_data()
#     phone = data['phone']
#     fio = data['fio']

#     add_user(user_id=message.from_user.id, phone=phone, fio=fio, email=email)

#     await state.finish()
#     await message.answer("Siz muafaqatli royxatdan otdingiz!", reply_markup=menu_buttons)
#     await UserStates.menu.set()


# @dp.message_handler(lambda message: not message.text.endswith('@gmail.com'), state=UserStates.get_email)
# async def invalid_email(message: types.Message):
#     await message.answer("Iltimos, faqat @gmail.com bilan tugaydigan emailni kiriting.")



# @dp.message_handler(lambda message: message.text == "Xonalarni bron qilish")
# async def empty_rooms(message: types.Message):
#     buttons = {
#         InlineKeyboardButton("💺 Ekonom", callback_data="empty_economy_0"),
#         InlineKeyboardButton("🏨 Standart", callback_data="empty_standard_0"),
#         InlineKeyboardButton("🌟 Komfort", callback_data="empty_comfort_0"),
#         InlineKeyboardButton("💼 Biznes", callback_data="empty_business_0"),
#         InlineKeyboardButton("👑 VIP", callback_data="empty_vip_0"),
#     }
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     await message.answer("Bo'sh xonalarni ko'rish uchun xonalar sinfini tanlang:", reply_markup=keyboard)


# @dp.callback_query_handler(lambda call: call.data.startswith("empty_"))
# async def select_empty_class(call: types.CallbackQuery):
#     room_class = call.data.split("_")[1]
#     page = int(call.data.split("_")[2])
#     rooms = get_rooms("empty_rooms", room_class)

#     current_page_rooms = get_paged_rooms(rooms, page)

#     buttons = []
#     for room in current_page_rooms:
#         buttons.append(InlineKeyboardButton(f"🛏️ Xona {room[1]}", callback_data=f"room_{room[1]}"))

#     keyboard = InlineKeyboardMarkup(row_width=1)
#     keyboard.add(*buttons)

#     if page > 0:
#         keyboard.add(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"empty_{room_class}_{page - 1}"))

#     if len(rooms) > (page + 1) * ROOMS_PER_PAGE:
#         keyboard.add(InlineKeyboardButton("➡️ Keyingi", callback_data=f"empty_{room_class}_{page + 1}"))

#     if room_class == "economy":
#         with open("images/econom-class-room.jpg", "rb") as photo:
#             await call.message.answer_photo(photo, caption=description_for_eco, reply_markup=keyboard)
#     elif room_class == "standard":
#         with open("images/standart-class-room.jpg", "rb") as photo:
#             await call.message.answer_photo(photo, caption=description_for_standart, reply_markup=keyboard)
#     elif room_class == "comfort":
#         with open("images/comfort-class-room.jpg", "rb") as photo:
#             await call.message.answer_photo(photo, caption=description_for_comfort, reply_markup=keyboard)
#     elif room_class == "business":
#         with open("images/business-class-room.jpg", "rb") as photo:
#             await call.message.answer_photo(photo, caption=description_for_business, reply_markup=keyboard)
#     elif room_class == "vip":
#         with open("images/vip-class-room.jpg", "rb") as photo:
#             await call.message.answer_photo(photo, caption=description_for_vip, reply_markup=keyboard)


# @dp.callback_query_handler(lambda call: call.data.startswith("room_"))
# async def select_room(call: types.CallbackQuery):
#     room_number = int(call.data.split("_")[1])
#     buttons = [
#         InlineKeyboardButton("-", callback_data=f"decrease_{room_number}_2"),
#         InlineKeyboardButton("2", callback_data=f"static_{room_number}_2"),
#         InlineKeyboardButton("+", callback_data=f"increase_{room_number}_2"),
#         InlineKeyboardButton("Bron qilish", callback_data=f"book_{room_number}_2"),
#     ]
#     keyboard = InlineKeyboardMarkup(row_width=3)
#     keyboard.add(*buttons)
#     await call.message.answer(f"Xona {room_number}. Iltimos, odamlar sonini tanlang:", reply_markup=keyboard)



# @dp.callback_query_handler(lambda call: call.data.startswith(("increase_", "decrease_", "book_")))
# async def manage_people(call: types.CallbackQuery):
#     action, room_number, people = call.data.split("_")
#     room_number = int(room_number)
#     people = int(people)

#     if action == "increase":
#         people += 1
#     elif action == "decrease":
#         if people > 1:
#             people -= 1
#     elif action == "book":
#         user_id = call.from_user.id
#         move_room_to_booked(user_id, room_number, people)
#         await call.message.answer(f"Xona {room_number} {people} kishiga muvaffaqiyatli bron qilindi.")
#         return

#     buttons = [
#         InlineKeyboardButton("-", callback_data=f"decrease_{room_number}_{people}"),
#         InlineKeyboardButton(str(people), callback_data=f"static_{room_number}_{people}"),
#         InlineKeyboardButton("+", callback_data=f"increase_{room_number}_{people}"),
#         InlineKeyboardButton("Bron qilish", callback_data=f"book_{room_number}_{people}"),
#     ]
#     keyboard = InlineKeyboardMarkup(row_width=3)
#     keyboard.add(*buttons)
#     await call.message.edit_reply_markup(reply_markup=keyboard)


# @dp.message_handler(text="Maning bronlarim")
# async def get_history(message: Message):
#     user_id = message.from_user.id
#     print(f"User ID: {user_id}")

#     cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
#     current_user = cursor.fetchone()

#     if current_user:
#         user_data = f"Sizning malumotlariz:\nTelefon raqam: {current_user[1]}\nToliq Ism (F.I.O): {current_user[2]}\nEmail: {current_user[3]}"

#         cursor.execute("SELECT room_number, room_class, people_count FROM booked_rooms WHERE user_id = ?", (user_id,))
#         booked_rooms = cursor.fetchall()

#         if booked_rooms:
#             rooms_info = "\n\nSizning bronlangan xonalariz:\n"
#             for room in booked_rooms:
#                 rooms_info += f"Xona raqami: {room[0]}, Hotel LVL: {room[1]}, Odamlar soni: {room[2]}\n"
#         else:
#             rooms_info = "\n\nSizda bronlangan xonalar mavjud emas ."

#         await message.answer(user_data + rooms_info)
#     else:
#         await message.answer("Malumot topilmadi!")


# @dp.message_handler(text="Mexmonxonani baholash")
# async def rate_handler(message: types.Message):
#     user_id = message.from_user.id

#     cursor.execute("SELECT rating FROM ratings WHERE user_id = ?", (user_id,))
#     if cursor.fetchone():
#         # Calculate the average rating
#         cursor.execute("SELECT AVG(rating) FROM ratings")
#         average_rating = cursor.fetchone()[0]

#         await message.answer(f"📊 Siz allaqachon baho bergansiz. Rahmat!\n"
#                              f"📈 Hozirgi o'rtacha baho: {round(average_rating, 2)}")
#     else:
#         await message.answer("🌟 Iltimos, reytingingizni tanlang:", reply_markup=star_choose)

# @dp.callback_query_handler(lambda call: call.data.startswith("rate_"))
# async def rate_callback(call: types.CallbackQuery):
#     user_id = call.from_user.id
#     rating = int(call.data.split("_")[1])

#     cursor.execute("SELECT rating FROM ratings WHERE user_id = ?", (user_id,))
#     if cursor.fetchone():
#         cursor.execute("SELECT AVG(rating) FROM ratings")
#         average_rating = cursor.fetchone()[0]

#         await call.answer(f"📊 Siz allaqachon baho bergansiz.\n"
#                           f"📈 Hozirgi o'rtacha baho: {round(average_rating, 2)}", show_alert=True)
#         return

#     cursor.execute("INSERT INTO ratings (user_id, rating) VALUES (?, ?)", (user_id, rating))
#     connect.commit()

#     cursor.execute("SELECT AVG(rating) FROM ratings")
#     average_rating = cursor.fetchone()[0]

#     await call.message.answer(f"🌟 Siz {rating} baho berdingiz.\n📈 Hozirgi o'rtacha baho: {round(average_rating, 2)}")
#     await call.answer()

# if __name__ == '__main__':
#     start_polling(dp, skip_updates=True)
