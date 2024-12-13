from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, WebAppInfo


send_phone_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Iltimos, telefon  raqamingizni jonating",request_contact=True)
        ]
    ],resize_keyboard=True, one_time_keyboard=True

)

menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Xonalarni bron qilish"),
            KeyboardButton(text="Maning bronlarim"),
            KeyboardButton(text="Mehmonxona haqida", web_app=WebAppInfo(url="https://hotel-uz.com/uz/booking/"))
        ],
        [
            KeyboardButton(text="Mexmonxonani baholash")
        ]
    ],resize_keyboard=True
)