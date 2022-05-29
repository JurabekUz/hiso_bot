import datetime
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from data.config import ADMINS
from keyboards.default.services_board import services_menu
from loader import dp, db, bot
from keyboards.inline.menu_boards import oylar_menu, Select_menu
from keyboards.inline.callback_data import create_callback, select_callback, oylar_callback
from states.states import AuthState, DateState, HisobotState
from aiogram.types import ReplyKeyboardRemove

from . hisobot_handler import xabar, savollar

#istisnolar
@dp.message_handler(state=DateState.all_states, text = '📋 Hisobot topshirish',user_id=ADMINS)
@dp.message_handler(state=HisobotState.all_states, text = '📋 Hisobot topshirish',user_id=ADMINS)
async def hisobot_form(message: types.Message, state: FSMContext):
    await message.answer(savollar[0],reply_markup=ReplyKeyboardRemove())
    await HisobotState.zayafka.set()

@dp.message_handler(text="/allusers", user_id=ADMINS, state=AuthState.logined)
async def get_all_users(message: types.Message):
    users = await db.select_all_users()
    msg = "Hamma Xodimlar\n"
    print(users)
    i=1
    for user in users:
        msg += f"{i}. {user[1]} {user[2]}\n"
        i+=1
    await message.answer(msg)

@dp.message_handler(text="/allusers", user_id=ADMINS, state=DateState.all_states)
async def error_def(message: types.Message):
    await message.reply("Iltimos Amalni To'g'ri Davom Ettiring")

@dp.message_handler(text="/cleandb", user_id=ADMINS, state=AuthState.logined)
async def get_all_users(message: types.Message):
    await db.delete_users()
    await message.answer("Xodimlar bazadan o'chirildi!")

@dp.callback_query_handler(create_callback.filter(action='create'),user_id=ADMINS, state="*")
async def tasdiqlash(call: CallbackQuery):
    await call.answer("Siz ushbu hisobotni tasdiqladingiz. Hisobot Yaratildi", cache_time=60, show_alert=True)
    await  call.message.edit_reply_markup()

@dp.callback_query_handler(create_callback.filter(action='cancel'),user_id=ADMINS, state="*")
async def bekorqilish(call: CallbackQuery, callback_data:dict):
    hisobot_id = int(callback_data.get('hisobot_id'))
    xodim_id = int(callback_data.get('xodim_id'))
    print(xodim_id)
    await db.delete_hisobot(id=hisobot_id)
    await bot.send_message(chat_id=xodim_id,text="⛔️Sizning hisobotingiz rad etildi. Iltimos uni tekshirib qaytadan kiriting")
    await call.answer(f"Siz ushbu hisobotni rad qildingiz. Hisobot bekor qilindi", cache_time=60, show_alert=True)
    await  call.message.edit_reply_markup()

@dp.message_handler(commands=['oylik','haftalik','kunlik'],state=DateState.all_states, user_id=ADMINS)
@dp.message_handler(commands=['oylik','haftalik','kunlik'], user_id=ADMINS,state=AuthState.logined)
async def get_all_users(message: types.Message, state: FSMContext):
    komanda = message.get_command()
    if komanda == '/haftalik':
        await DateState.week.set()
        msg = "Xodimlar\n"
        users = await db.select_all_users()
        for user in users:
            msg += f"{user[1]} {user[2]} - /{user[0]}\n"
        await message.answer("Bitta Xodim uchun mos kamandadan foydalaning\n"
                             "Hamma Xodimlar uchun /hamma komandasi ishlaydi")
        await message.answer(msg)

    elif komanda == "/oylik":
        await DateState.month.set()
        await message.answer("Oylik hisobotlarini olish uchun oyni kiriting\n",reply_markup=oylar_menu)
    elif komanda == "/kunlik":
        await DateState.days.set()
        await message.answer("Kunlik hisobotlarini olish uchun sana kiriting\n Masalan: 2022-12-30",reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=DateState.days, user_id=ADMINS)
async def get_day_user(message: types.Message, state: FSMContext):
    sana = message.text
    await state.update_data(sana=sana)
    msg = "Xodimlar\n"
    users = await db.select_all_users()
    for user in users:
        msg += f"{user[1]} {user[2]} - /{user[0]}\n"
    await message.answer("Bitta Xodim uchun mos kamandadan foydalaning\n"
                         "Hamma Xodimlar uchun /hamma komandasi ishlaydi")
    await message.answer(msg)
    await DateState.xodim_kun.set()

@dp.message_handler(state=DateState.xodim_kun,user_id=ADMINS)
async def get_day_user(message: types.Message, state:FSMContext):
    msg = message.get_command()
    data = await state.get_data()
    sana = data.get('sana')
    sana = sana.split('-')
    sana = datetime.date(year=int(sana[0]), month=int(sana[1]), day=int(sana[2]))
    if message.text=='/hamma':
        result = "Hamma Xodimlarning Hisobotlari\n"
        hisobotlar = await db.select_days_hisobot(sana=sana)
        xodimlar = await db.select_all_users()
        for hisobot in hisobotlar:
            for xodim in xodimlar:
                if hisobot[1]==xodim[0]:
                    result = f"Xodim: {xodim[1]} {xodim[2]}\n"
                    for i in range(15):
                        result += f"{xabar[i]} {hisobot[i + 3]}\n"
                    result += f"Sana: {sana}\n\n"
        await message.answer(result)
        await message.answer(
            "1.Boshqa Xodim tanlashingiz mumkin\n2.Bosh menuga yoki orqaga qaytish uchun tugmalardan foydalaning",
            reply_markup=Select_menu)
    else:
        msg = msg.split('/')  # ['/','user_id']
        try:
            user_id = int(msg[1])
            hisobotlar = await db.select_days_hisobot(user_id=user_id,sana=sana)
            xodim = await db.select_user(id=user_id)
            result = f"Xodim: {xodim[1]} {xodim[2]}\n"
            for hisobot in hisobotlar:
                for i in range(15):
                    result += f"{xabar[i]} {hisobot[i + 3]}\n"
                result += f"Sana: {sana}\n\n"
            await message.answer(result)
            await message.answer(
                "1.Boshqa Xodim tanlashingiz mumkin\n2.Bosh menuga yoki orqaga qaytish uchun tugmalardan foydalaning",
                reply_markup=Select_menu)
        except:
            await message.reply("Iltimos botdan to'g'ri foydalaning!!!\n"
                                "Ko'rsatilgan komandalarni ishlating")



@dp.callback_query_handler(oylar_callback.filter(),state=DateState.month, user_id=ADMINS)
async def get_month_user(call: types.CallbackQuery, callback_data:dict, state: FSMContext):
    logging.info(f"{callback_data=}")
    oy = callback_data['item_name']
    print(oy)
    await state.update_data(oy=oy)
    msg = "Xodimlar\n"
    users = await db.select_all_users()
    for user in users:
        msg += f"{user[1]} {user[2]} - /{user[0]}\n"
    await call.message.answer("Bitta Xodim uchun mos kamandadan foydalaning\n"
                         "Hamma Xodimlar uchun /umumiy_hamma komandasi ishlaydi\n"
                          "Hamma Xodimlarni Alohida Ko'rish uchun /alohida_hamma komandasi ishlaydi")
    await call.message.delete()
    await call.message.answer(msg,reply_markup=ReplyKeyboardRemove())
    await DateState.xodim_oy.set()

@dp.message_handler(state=DateState.xodim_oy,user_id=ADMINS)
async def get_day_user(message: types.Message, state:FSMContext):
    msg = message.get_command()
    data = await state.get_data()
    oy = data.get('oy')
    sana1 = datetime.date(year=2022, month=int(oy), day=1)
    sana2 = datetime.date(year=2022, month=int(oy), day=31)
    if msg == '/umumiy_hamma':
        response = await db.select_all_between_hisobot(sana1=sana1, sana2=sana2)
        result="Barcha Xodimlar Yig'indi Hisobotlari\n"
        for i in range(15):
            result += f"{xabar[i]} {response[i]}\n"
        await message.answer(result)
    elif msg == "/alohida_hamma":
        res_group_by = await db.select_group_by_between_hisobot(sana1=sana1, sana2=sana2)
        for user in res_group_by:
            xodim = await db.select_user(id=user[0])
            result_gr = f"Xodim: {xodim[1]} {xodim[2]}\n"
            for i in range(15):
                result_gr += f"{xabar[i]} {user[i + 1]}\n"
            await message.answer(result_gr)
    else:
        msg = msg.split('/')  # ['/','user_id']
        try:
            user_id = int(msg[1])
            response = await db.select_between_hisobot(user_id=user_id, sana1=sana1, sana2=sana2)
            xodim = await db.select_user(id=user_id)
            result = f"Xodim: {xodim[1]} {xodim[2]}\n"
            for i in range(15):
                result += f"{xabar[i]} {response[i + 1]}\n"
            await message.answer(result)
        except:
            await message.reply("Iltimos botdan to'g'ri foydalaning!!!\n"
                                "Ko'rsatilgan komandalarni ishlating")
    await message.answer("1.Boshqa Xodim tanlashingiz mumkin")

#____________________________

@dp.callback_query_handler(select_callback.filter(name='go_head'),state=DateState.xodim_kun,user_id=ADMINS)
async def go_head_menu(call: types.CallbackQuery, callback_data:dict, state: FSMContext):
    msg = "<b>Shaxsiy Profil</b> \n📋 Hisobot topshirish \n⚙️Sozlash \n📈 Statistika"
    await call.message.delete()
    await call.message.answer(msg, reply_markup=services_menu)
    await AuthState.logined.set()

@dp.callback_query_handler(select_callback.filter(name='goback'),state=DateState.xodim_kun,user_id=ADMINS)
async def go_back_def(call: types.CallbackQuery, callback_data:dict, state: FSMContext):
    await DateState.days.set()
    await call.message.delete()
    await call.message.answer("Kunlik hisobotlarini olish uchun sana kiriting\n Masalan: 2022-12-30")


@dp.message_handler(state=DateState.week,user_id=ADMINS)
async def get_week_hisobot(message: types.Message):
    msg = message.get_command()
    today = datetime.date.today()
    weekday = today.weekday()
    year = today.year
    month = today.month
    hafta_boshi = datetime.date(year=year, month=month, day=today.day - weekday)
    print(hafta_boshi)
    if message.text == '/hamma':
        response = await db.select_all_between_hisobot(sana1=hafta_boshi, sana2=today)
        result = "Barcha Xodimlarning Haftalik Hisobotlar Yig'indi\n"
        for i in range(15):
            result += f"{xabar[i]} {response[i]}\n"
        await message.answer(result)
    else:
        msg = msg.split('/')  # ['/','user_id']
        try:
            user_id = int(msg[1])
            response = await db.select_between_hisobot(user_id=user_id, sana1=hafta_boshi, sana2=today)
            xodim = await db.select_user(id=user_id)
            result = f"Xodim: {xodim[1]} {xodim[2]}\n"
            for i in range(15):
                result += f"{xabar[i]} {response[i + 1]}\n"
            await message.answer(result)
        except:
            await message.reply("Iltimos botdan to'g'ri foydalaning!!!\n"
                                "Ko'rsatilgan komandalarni ishlating")
