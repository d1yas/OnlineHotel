# import sqlite3
# from aiogram.dispatcher.filters.builtin import CommandStart
# from keyboards.default.def_menu import choose_class_button
# from loader import dp
# from aiogram import  types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from database import *
# from describe import *
#
#
# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     buttons = [
#         types.KeyboardButton("Xonalarni bron qilish"),
#         types.KeyboardButton("Mehmonxona haqida"),
#     ]
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*buttons)
#     await message.answer("Iltimos, biror bir variantni tanlang:", reply_markup=keyboard)
#
# @dp.message_handler(lambda message: message.text == "Xonalarni bron qilish")
# async def empty_rooms(message: types.Message):
#     buttons = [
#         InlineKeyboardButton("💺 Ekonom", callback_data="empty_economy"),
#         InlineKeyboardButton("🏨 Standart", callback_data="empty_standard"),
#         InlineKeyboardButton("🌟 Komfort", callback_data="empty_comfort"),
#         InlineKeyboardButton("💼 Biznes", callback_data="empty_business"),
#         InlineKeyboardButton("👑 VIP", callback_data="empty_vip"),
#     ]
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     await message.answer("Bo'sh xonalarni ko'rish uchun xonalar sinfini tanlang:", reply_markup=keyboard)
#
#
# @dp.callback_query_handler(lambda call: call.data.startswith("empty_"))
# async def select_empty_class(call: types.CallbackQuery):
#     room_class = call.data.split("_")[1]
#     rooms = get_rooms("empty_rooms", room_class)
#     if not rooms:
#         await call.message.answer(f"{room_class} sinfida bo'sh xona mavjud emas.")
#         return
#
#     buttons = []
#     for room in rooms:
#         buttons.append(InlineKeyboardButton(f"🛏️ Xona {room[1]}", callback_data=f"room_{room[1]}"))
#     keyboard = InlineKeyboardMarkup(row_width=1)
#     keyboard.add(*buttons)
#
#
#     if call.data == "empty_economy":
#         with open("images/econom-class-room.jpg", "rb") as photo:
#             await call.message.answer_photo(photo, caption=description_for_eco, reply_markup=keyboard)
#     elif call.data == "empty_standard":
#         with open("images/standart-class-room.jpg", "rb") as photo:
#             await call.message.answer_photo(photo, caption=description_for_standart, reply_markup=keyboard)
#     elif call.data == "empty_comfort":
#         with open("images/comfort-class-room.jpg", "rb") as photo:
#             await call.message.answer_photo(photo, caption=description_for_comfort, reply_markup=keyboard)
#     elif call.data == "empty_business":
#         with open("images/business-class-room.jpg", "rb") as photo:
#             await call.message.answer_photo(photo, caption=description_for_business, reply_markup=keyboard)
#     elif call.data == "empty_vip":
#         with open("images/vip-class-room.jpg", "rb") as photo:
#             await call.message.answer_photo(photo, caption=description_for_vip, reply_markup=keyboard)
#
#
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
#
# @dp.callback_query_handler(lambda call: call.data.startswith(("increase_", "decrease_", "book_")))
# async def manage_people(call: types.CallbackQuery):
#     action, room_number, people = call.data.split("_")
#     room_number = int(room_number)
#     people = int(people)
#
#     if action == "increase":
#         people += 1
#     elif action == "decrease":
#         if people > 1:
#             people -= 1
#     elif action == "book":
#         move_room_to_booked(room_number, people)
#         await call.message.answer(f"Xona {room_number} {people} kishiga muvaffaqiyatli bron qilindi.")
#         return
#
#     buttons = [
#         InlineKeyboardButton("-", callback_data=f"decrease_{room_number}_{people}"),
#         InlineKeyboardButton(str(people), callback_data=f"static_{room_number}_{people}"),
#         InlineKeyboardButton("+", callback_data=f"increase_{room_number}_{people}"),
#         InlineKeyboardButton("Bron qilish", callback_data=f"book_{room_number}_{people}"),
#     ]
#     keyboard = InlineKeyboardMarkup(row_width=3)
#     keyboard.add(*buttons)
#     await call.message.edit_reply_markup(reply_markup=keyboard)

