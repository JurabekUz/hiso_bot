import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loader import dp, bot, db
from datetime import  date

from keyboards.inline.callback_data import confirm_callback, savollar_callback, create_callback
from keyboards.inline.menu_boards import  confirm_menu, savollar_menu, remove_and_create
from keyboards.default.services_board import services_menu
from states.states import RegisterState, AuthState, HisobotState
from data.config import ADMINS


# Hisobot to'dirishdagi savollar
savollar = [
    "1. Zayavkalar soni?", "2. Nechta gaplashdingiz?", "3. Sotilgan mahsulotlar soni?",
    "4. Teliga tushib bo'lmagan mijozlar soni?", "5. Noto'g'ri raqamlar soni?",
    "6. Buyurtma bermagan yoki adashgan mijozlar soni?", "7. Otkazlar soni?",
    "8. Naqd to'lovlar soni?", "9. Click orqali to'lovlar soni?",
    "10. Boshqa usuldagi to'lovlar soni?","11. Maxsus narxda sotilgan mahsulotlar soni? ",
    "12. Ehson qilingan mahsulotlar soni? ", "13. Sotilgan mahsulotlar soni?",
    "14. Sotib olgan mijozlar soni?", "15. Summa?",
    ]

#hisobot = []

fields = [
    'zayafka',
    'gaplashilgan',
    'sotilgan' ,
    'tel_tushmagan' ,
    'xato_nomer' ,
    'berma_adash' ,
    'otkaz',
    'naqt',
    'click',
    'boshqacha_tolov' ,
    'maxsus_narx',
    'ehson',
    'sotilgan2',
    'mijozlar',
    'summa',
]

xabar = [
        "📥 Zayavkalar soni:",
        "📞 Gaplashildi:",
        "✅ Sotilgan mahsulotlar soni:",
       " 🚫 Teliga tushib bo'lmagan mijozlar soni:",
        "#⃣ Noto'g'ri raqamlar soni:" ,
        "⛔️ Buyurtma bermagan yoki adashgan mijozlar soni:",
        "❌ Otkazlar soni:",
        "💵 Naqd to'lovlar soni:" ,
        "💳 Click orqali to'lovlar soni:",
        "🪙 Boshqa usuldagi to'lovlar soni:",
        "🏷 Maxsus narxda sotilgan mahsulotlar soni:",
        "❤️ Ehsonlar soni:",
        
        "☑️ Sotilgan mahsulotlar soni:",
        "🙋🏻 Sotib olgan mijozlar soni:",
        "💰 Summa:",
]

#magan_hisobot=''

# Hisobot to'ldirish  -------------------------------------------------------
@dp.message_handler(state=AuthState.logined, text = '📋 Hisobot topshirish')
async def hisobot_form(message: types.Message, state: FSMContext):
    await message.answer(savollar[0],reply_markup=ReplyKeyboardRemove())
    await HisobotState.zayafka.set()

@dp.message_handler(state=HisobotState.zayafka)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'zayafka': count }
        )
        await message.answer(savollar[1])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.gaplashilgan)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'gaplashilgan': count }
        )
        await message.answer(savollar[2])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.sotilgan)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'sotilgan': count }
        )
        await message.answer(savollar[3])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.tel_tushmagan)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'tel_tushmagan': count }
        )
        await message.answer(savollar[4])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.xato_nomer)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'xato_nomer': count }
        )
        await message.answer(savollar[5])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.berma_adash)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'berma_adash': count }
        )
        await message.answer(savollar[6])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.otkaz)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'otkaz': count }
        )
        await message.answer(savollar[7])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.naqt)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'naqt': count }
        )
        await message.answer(savollar[8])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.click)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'click': count }
        )
        await message.answer(savollar[9])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.boshqacha_tolov)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'boshqacha_tolov': count }
        )
        await message.answer(savollar[10])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.maxsus_narx)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'maxsus_narx': count }
        )
        await message.answer(savollar[11])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.ehson)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'ehson': count }
        )
        await message.answer(savollar[12])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.sotilgan2)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'sotilgan2': count }
        )
        await message.answer(savollar[13])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.mijozlar)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        await state.update_data(
            {'mijozlar': count }
        )
        await message.answer(savollar[14])
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.message_handler(state=HisobotState.summa)
async def hisobot_form(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = await db.select_user(id=user_id)
    first_name=user[1]
    last_name = user[2]
    count = message.text
    if count.isnumeric():
        await state.update_data({'summa': count, "first_name": first_name, "last_name" : last_name })
        sonlar = [] #bazaga shu orqali qoshamiz
        magan_hisobot = f"👩🏻‍💻Operator: {first_name} {last_name}\n"
        data = await state.get_data()
        i=0
        for field in fields:
            magan_hisobot += f"{xabar[i]} {data.get(field)}\n"
            sonlar.append(data.get(field))
            i+=1
        await state.update_data(hiso=sonlar)
        await state.update_data(text=magan_hisobot)
        await message.answer(magan_hisobot)
        await message.answer("Ushbu ma'lumotlar to'g'rimi",reply_markup=confirm_menu)
        await HisobotState.next()
    else:
        await message.reply('Iltimos son kiriting!')

@dp.callback_query_handler(confirm_callback.filter(item_name='correct'),state=HisobotState.tasdiqlash)
async def hisobot_form(call: types.CallbackQuery,callback_data: dict, state: FSMContext):
    # logging yordamida foydalanuvchidan qaytgan callback ni ko'ramiz
    #logging.info(f"{callback_data=}")
    #hisobotni adminga yuborish
    data = await state.get_data()
    hiso = data.get('hiso') #listda saqlangan vasollarning qiymatlari
    xabar = data.get('text')
    user_id=call.from_user.id
    kun = date.today()
    new_hisobot = await db.add_hisobot(
        user_id=user_id,
        sana= kun,
        zayafka = hiso[0],
        gaplashilgan = hiso[1],
        sotilgan = hiso[2],
        tel_tushmagan = hiso[3],
        xato_nomer = hiso[4],
        berma_adash = hiso[5],
        otkaz = hiso[6],
        naqt = hiso[7],
        click = hiso[8],
        boshqacha_tolov = hiso[9],
        maxsus_narx = hiso[10],
        ehson = hiso[11],
        sotilgan2 = hiso[12],
        mijozlar =  hiso[13],
        summa = hiso[14],
    )
    hisobot_id = new_hisobot[0]
    print(hisobot_id)
    sana = f"_______________________\nHisobot sanasi: {date.today()}\nHisobot id: {hisobot_id}"
    tugmalar = await remove_and_create(hisobot_id=hisobot_id, xodim_id=user_id)
    await bot.send_message(ADMINS[0],xabar+sana,reply_markup=tugmalar)
    await call.message.delete()
    await call.message.answer("✅ Hisobot yuborildi",reply_markup=services_menu)
    await call.answer(cache_time=60)
    await state.finish()
    await AuthState.logined.set()



@dp.callback_query_handler(confirm_callback.filter(item_name='incorrect'),state=HisobotState.tasdiqlash)
async def hisobot_form(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("❗️ Ma'lumotlarni to'liq qaytadan kiritish uchun <b>Hisobot To'ldirish</b> tugmasini bo'sing\n"
                              "Agar malumotni qisman to'g'irlamoqchi bo'lsangiz o'sha savolning raqamini kiriting:1 dan 15 gacha"
                              , reply_markup=savollar_menu)
    await call.answer(cache_time=60)

@dp.callback_query_handler(savollar_callback.filter(item_name='qayta'),state=HisobotState.tasdiqlash)
async def hisobot_form(call: types.CallbackQuery, callback_data: dict,state: FSMContext):
    await state.finish()
    await call.message.answer(savollar[0])
    await HisobotState.zayafka.set()

@dp.callback_query_handler(savollar_callback.filter(),state=HisobotState.tasdiqlash)
async def hisobot_form(call: types.CallbackQuery, callback_data: dict,state: FSMContext):
    #callbackni olamiz
    #callback_text = callback_data['text'] # str qiymat
    title = call.data.title()
    splited_list = title.split(':')
    number = splited_list[1]
    number = int(number)-1
    print(number)
    await state.update_data(
        {'number': number}
    )
    await HisobotState.qayta_kirit.set()
    await call.message.delete()
    await call.message.answer(savollar[number])
    await call.answer(cache_time=60)


@dp.message_handler(state=HisobotState.qayta_kirit)
async def hisobot_form(message: types.Message, state: FSMContext):
    count = message.text
    if count.isnumeric():
        data = await state.get_data()
        number = data.get('number')
        last_name= data.get('last_name')
        first_name= data.get('first_name')
        new_field = fields[number]
        print(new_field)
        hiso = data.get('hiso')
        hiso[number]=count
        await state.update_data(
            data={
                "hiso":hiso,
                new_field : count
            }
        )
        #fieldni olyapmiz
        magan_hisobot = f"👩🏻‍💻Operator: {first_name} {last_name} \n"
        new_data = await state.get_data()
        i = 0
        for field in fields:
            magan_hisobot += f"{xabar[i]} {new_data.get(field)}\n"
            i += 1

        await state.update_data(text=magan_hisobot)
        await message.answer(magan_hisobot)
        await message.answer("Ushbu ma'lumotlar to'g'rimi", reply_markup=confirm_menu)
        await HisobotState.tasdiqlash.set()
    else:
        await message.reply('Iltimos son kiriting!')

