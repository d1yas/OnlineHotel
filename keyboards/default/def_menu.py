from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


send_phone_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Iltimos, telefon  raqamingizni jonating",request_contact=True)
        ]
    ],resize_keyboard=True, one_time_keyboard=True

)

