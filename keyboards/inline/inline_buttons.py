from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo



# choose_menu_buttons = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Nomer bron qilish."),
#             InlineKeyboardButton(text="Mening bron qilingan xonalarim.")
#         ],
#         [
#             InlineKeyboardButton(text="Mexmonxona xizmatlari."),
#         ]
#     ]
# )


star_choose = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("⭐", callback_data="rate_1"),
            InlineKeyboardButton("⭐⭐", callback_data="rate_2"),
            InlineKeyboardButton("⭐⭐⭐", callback_data="rate_3"),
        ],
        [
            InlineKeyboardButton("⭐⭐⭐⭐", callback_data="rate_4"),
            InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="rate_5"),
        ]
    ]
)


confirm_buttons = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm_booking"),
    InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_booking")
)
