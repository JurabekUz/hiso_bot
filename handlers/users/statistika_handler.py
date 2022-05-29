from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from data.config import ADMINS
from states.states import AuthState

@dp.message_handler(state=AuthState.logined, text = '📈 Statistika',user_id=ADMINS)
async def statistika(message: types.Message, state: FSMContext):
    sotilgan = await db.st_sotilgan()
    gaplashilgan = await db.st_gaplashilgan()
    users = await db.select_all_users()
    gap = "Gaplashilgan Soni Bo'yicha Statistika\n"
    sot = "Sotilgan Mahsulotlar Soni Bo'yicha Statistika\n"
    i=1
    for item in sotilgan:
        user_id=item[0]
        count = item[1]
        for user in users:
            if user[0]==user_id:
                sot += f"{i}. {user[1]} {user[2]}: {count} \n"
                i+=1
                break
    j=1
    for item in gaplashilgan:
        user_id=item[0]
        count = item[1]
        for user in users:
            if user[0]==user_id:
                gap += f"{j}. {user[1]} {user[2]}: {count} \n"
                j+=1
                break
    await message.answer(sot)
    await message.answer(gap)

@dp.message_handler(state=AuthState.logined, text = '📈 Statistika')
async def statistika(message: types.Message):
    sotilgan = await db.st_sotilgan()
    gaplashilgan = await db.st_gaplashilgan()
    user_id=message.from_user.id
    gap = "Gaplashilgan Mijozlar Soni Bo'yicha Statistika\n"
    sot = "Sotilgan Mahsulotlar Soni Bo'yicha Statistika\n"

    i=1
    for item in sotilgan:
        item_id=item[0]
        count = item[1]
        if item_id==user_id:
            response = f"Siz {i}-o'rindasiz\n" \
                   f"{count} ta mahsulot sotgansiz \n"
            await message.answer(sot+response)
        i+=1

    j=1
    for item in gaplashilgan:
        id=item[0]
        count = item[1]
        if id==user_id:
            response = f"Siz {j}-o'rindasiz\n" \
                        f"{count}-ta mijozlar bilan gaplashganisiz \n"
            await message.answer(gap+response)
        j+=1


