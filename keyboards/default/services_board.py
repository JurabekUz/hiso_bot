from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

services_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📋 Hisobot topshirish')
        ],
        [
            KeyboardButton(text='⚙️ Sozlash'),
            KeyboardButton(text='📈 Statistika'),

        ],
    ],
    resize_keyboard=True
)

Numboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Telefon Raqam", request_contact=True)
        ]
    ]
    )