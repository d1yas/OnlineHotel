from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo



choose_menu_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Nomer bron qilish."),
            InlineKeyboardButton(text="Mening bron qilingan xonalarim.")
        ],
        [
            InlineKeyboardButton(text="Mexmonxona xizmatlari."),
        ]
    ]
)