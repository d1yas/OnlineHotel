from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



choose_menu_v2 = InlineKeyboardMarkup(
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