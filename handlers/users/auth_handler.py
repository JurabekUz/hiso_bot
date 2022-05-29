from datetime import date

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import Passwords, ADMINS
from keyboards.inline.menu_boards import auth_menu, confirm_menu
from keyboards.default.services_board import services_menu, Numboard
from keyboards.inline.callback_data import auth_callback, confirm_callback
from states.states import RegisterState, AuthState

#istisnolar
@dp.message_handler(commands=['oylik','haftalik','kunlik','allusers'],state=RegisterState.all_states)
async def bot_echo(message: types.Message):
    await message.answer("Bu buyruqlar adminlar uchun. Iltimos botdan to'gri foydalaning\n Amalni davom ettiring")


# RO'YXATDAN O'TISH --------------------------------------------------------
# register tugmasi uchun
@dp.callback_query_handler(auth_callback.filter(item_name='register'))
async def user_register(call: types.CallbackQuery):
    await RegisterState.password.set()
    await call.message.answer("🤖 Iltimos parolni kiriting:")
    await call.message.delete()
    await call.answer(cache_time=60)

# register tugmasi uchun parol tekshirish
@dp.message_handler(state=RegisterState.password)
async def check_password(message: types.Message, state: FSMContext):
    password = message.text
    if password in Passwords:
        await  message.delete()
        await message.answer(f"✅ <b>TASDIQLANDI</b>")
        await message.answer("<i>Ismingizni kiriting</i>\n Masalan: Azamat")
        await RegisterState.next()
    else:
        await message.delete()
        await message.answer("❌ <b>NOTO'G'RI PAROL</b>")

@dp.message_handler(state=RegisterState.name)
async def register_form(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(
        {'name': name}
    )
    await message.answer("<i>Familiyangizni kiriting</i>\n Masalan: Karimov")
    await RegisterState.next()

@dp.message_handler(state=RegisterState.sure_name)
async def register_form(message: types.Message, state: FSMContext):
    sure_name = message.text
    await state.update_data(
        {'sure_name': sure_name}
    )
    await message.answer("<i> Tug'ilgan sanangizni kiriting</i>\n Masalan: 2002-12-23")
    await RegisterState.next()

@dp.message_handler(state=RegisterState.birthday)
async def register_form(message: types.Message, state: FSMContext):
    birthday = message.text
    await state.update_data(
        {'birthday': birthday}
    )
    await message.answer("<i>Telefon raqam kiriting yoki kontaktni ulashish</i>\n Masalan: 971234567",reply_markup=Numboard)
    await RegisterState.next()

@dp.message_handler(state=RegisterState.contact,content_types='contact')
async def answer_phnum(message: types.Message, state: FSMContext):
    contact=message.contact
    await state.update_data({
        "contact": contact['phone_number']})
    # Ma`lumotlarni qayta o'qiymiz
    data = await state.get_data()
    name = data.get('name')
    sure_name = data.get('sure_name')
    birthday = data.get('birthday')
    contact = data.get('contact')

    msg = "Quyidai ma`lumotlar qabul qilindi:\n"
    msg += f"Ism - {name}\n"
    msg += f"Familiya - {sure_name}\n"
    msg += f"Tug'ilgan sana - {birthday}\n"
    msg += f"Telefon: - {contact}"
    msg += "<b>Ushbu ma'lumotlar to'g'rimi?</b>"
    await message.answer(msg,reply_markup=confirm_menu)
    await RegisterState.next()


@dp.message_handler(state=RegisterState.contact)
async def register_form(message: types.Message, state: FSMContext):
    contact = message.text
    await state.update_data(
        {'contact': contact}
    )
    # Ma`lumotlarni qayta o'qiymiz
    data = await state.get_data()
    name = data.get('name')
    sure_name = data.get('sure_name')
    birthday = data.get('birthday')
    contact = data.get('contact')

    msg = "Quyidai ma`lumotlar qabul qilindi:\n"
    msg += f"Ism - {name}\n"
    msg += f"Familiya - {sure_name}\n"
    msg += f"Tug'ilgan sana - {birthday}\n"
    msg += f"Telefon: - {contact}\n"
    msg += "<b>Ushbu ma'lumotlar to'g'rimi?</b>"
    await message.answer(msg,reply_markup=confirm_menu)
    await RegisterState.next()

@dp.callback_query_handler(confirm_callback.filter(item_name='correct'),state=RegisterState.confirm)
async def register_form(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    sure_name = data.get('sure_name')
    birthday = data.get('birthday')
    contact = data.get('contact')
    # userni bazaga qo'shamiz
    birthday = birthday.split('-') #str ni datetype objectga o'tkazib olamiz
    birthday = date(year=int(birthday[0]),month=int(birthday[1]), day=int(birthday[2]))
    try:
        await db.add_user(id=call.from_user.id,
        first_name=name, last_name=sure_name, birthday=birthday, contact=contact)
        # Adminga xabar berish
        count = await db.count_users()
        msg = f"{name} {sure_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

        await state.finish()
        await AuthState.logined.set()
        await call.message.edit_reply_markup()
        await call.message.answer("✅ Ro'yxatdan o'tish muvoffaqiyatli yakunlandi.")
        msg = "<b>Shaxsiy Profil</b> \n📋 Hisobot topshirish \n⚙️Sozlash \n📈 Statistika"
        await call.message.answer(msg,reply_markup=services_menu)
        await call.answer(cache_time=60)

    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(id=call.from_user.id)
        print("bunday user bor")
        await call.message.answer("Siz oldin Ro'yxatdan o'tgansiz.\nIltimos Profilingizga kiring")
        await state.finish()

@dp.callback_query_handler(confirm_callback.filter(item_name='incorrect'),state=RegisterState.confirm)
async def register_form(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("❗️ Ma'lumotlarni qaytadan kiriting")
    await RegisterState.name.set()
    await call.message.answer("<i>Ismingizni kiriting</i>\n Masalan: Azamat")


# Kirish  --------------------------------------------------------------------
# login tugmasi uchun
@dp.callback_query_handler(auth_callback.filter(item_name='login'))
async def user_register(call: types.CallbackQuery):
    await AuthState.password.set()
    await call.message.answer("🤖 Iltimos parolni kiriting:")
    await call.message.delete()
    await call.answer(cache_time=60)

# login tugmasi uchun parol tekshirish
@dp.message_handler(state=AuthState.password)
async def check_password(message: types.Message, state: FSMContext):
    password = message.text
    if password in Passwords:
        await  message.delete()
        await message.answer(f"✅TASDIQLANDI ")
        msg = "<b>Shaxsiy Profil</b> \n📋 Hisobot topshirish \n⚙️Sozlash \n📈 Statistika"
        await message.answer(msg, reply_markup=services_menu)
        await AuthState.logined.set()
    else:
        await message.delete()
        await message.answer("❌NOTO'G'RI PAROL")

@dp.message_handler(text="⚙️ Sozlash", state=AuthState.logined)
async def sozlash(msg: types.Message):
    await msg.answer("Bu qism hali qo'shilmagan")








