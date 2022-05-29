from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .callback_data import (auth_callback, confirm_callback, savollar_callback,
                            create_callback, oylar_callback, select_callback)

# auth menusi
auth_menu = InlineKeyboardMarkup(row_width=1)
register = InlineKeyboardButton(text="Ro'yxatdan o'tish", callback_data=auth_callback.new(item_name="register"))
auth_menu.insert(register)

login = InlineKeyboardButton(text="Profilga kirish", callback_data=auth_callback.new(item_name="login"))
auth_menu.insert(login)

# confirm menu si (tasdiqlash menusi)
confirm_menu = InlineKeyboardMarkup(row_width=2)
correct = InlineKeyboardButton(text="✅ TO'G'RI", callback_data=confirm_callback.new(item_name="correct"))
confirm_menu.insert(correct)

incorrect = InlineKeyboardButton(text="❌ NOTO'G'RI", callback_data=confirm_callback.new(item_name="incorrect"))
confirm_menu.insert(incorrect)

# qisman to'g'irlash uchun maenu
savollar_menu = InlineKeyboardMarkup(row_width=5)
for n in range(1,16):
    son = str(n)
    savollar_menu.insert(InlineKeyboardButton(text=son, callback_data=savollar_callback.new(item_name=son)))
savollar_menu.insert(InlineKeyboardButton(text="Hisobot To'ldirish", callback_data=confirm_callback.new(item_name='qayta')))

# Admin tasqilov menusi

async def remove_and_create(hisobot_id, xodim_id):
    create_remove_menu = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🆗 TASDIQLASHI", callback_data=create_callback.new(action="create",hisobot_id=hisobot_id, xodim_id=xodim_id)),
            InlineKeyboardButton(text="❌ RAD ETISH", callback_data=create_callback.new(action="cancel", hisobot_id=hisobot_id, xodim_id=xodim_id)),
        ]]
    )
    return create_remove_menu

oylar_menu = InlineKeyboardMarkup(row_width=3)
oylar = ['Yanvar','Fevral','Mart','Aprel','May','Iyun','Iyul','August','Sentabr','Oktabr','Noyabr','Dekabr']
oy_num = ['01','02','03','04','05','06','07','08','09','10','11','12']
for n in range(12):
    oylar_menu.insert(InlineKeyboardButton(text=oylar[n],callback_data=oylar_callback.new(item_name=oy_num[n])))

# select menu si (orqaga va boshmenu tugmalari)
Select_menu = InlineKeyboardMarkup(row_width=2)
head_menu = InlineKeyboardButton(text="Bosh Menu", callback_data=select_callback.new(name="go_head"))
Select_menu.insert(head_menu)

go_back = InlineKeyboardButton(text="Orqaga", callback_data=select_callback.new(name="goback"))
Select_menu.insert(go_back)