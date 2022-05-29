import asyncio

from utils.db_api.postgresql import Database
from datetime import date,datetime

async def test():
    db = Database()
    await db.create()

    #print("Users jadvalini yaratamiz...")
    #await db.drop_users()
    #await db.create_table_users()
    #await db.create_table_hisobot()
    #print("Yaratildi")

    print("Foydalanuvchilarni qo'shamiz")
    vaqt = date(year=2002,month=12,day=16)
    '''
    await db.add_user(2, "name2", "surename2", '98745621', vaqt)
    await db.add_user(3, "name3", "surename3", '98745621', vaqt)
    await db.add_user(4, "name4", "surename4", '98745621', vaqt)
    print("Qo'shildi")
    '''

    users = await db.select_all_users()
    print(f"Barcha foydalanuvchilar: {users[0]}")
    print(f"ism: {users[0][1]}")

    # user = await db.select_user(id=4)
    # print(f"Foydalanuvchi: {user[0]}")

    kun = date.today()
    #hiso = await db.add_hisobot(3,kun,12, 12, 16, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14,126)
    # await db.add_hisobot(3, kun, 5, 16, 16, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 126)
    # await db.add_hisobot(4, kun, 5, 10, 5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 126)
    # await db.add_hisobot(4, kun, 5, 10, 5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 126)
    # await db.add_hisobot(5, kun, 5, 12, 5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 126)
    # await db.add_hisobot(5, kun, 5, 13, 5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 126)
    # await db.add_hisobot(5,kun,5, 4, 13, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14,126)

    #dele = await db.delete_hisobot(id=10)

    soni = await  db.count_hisobot()
    print(soni) # 5 son qaytaradi

    user_soni = await db.count_users()
    print(user_soni) #5 son qaytaradi

    #hisobot jadvalidan user ga tegishli biror kundagi hisobotni olish uchun
    day_hisobot_user = await db.select_days_hisobot(user_id=2, sana=kun)
    print(day_hisobot_user[0][0]) # id sini korish uchun

    # hisobot jadvalidan biror kundagi hisobotni olish uchun
    day_hisobot = await db.select_days_hisobot(sana=kun)
    print(len(day_hisobot)) #list uzunligini olish

    sana1 = date(year=2022, month=5, day=1)
    sana2 = date(year=2022, month=5, day=31)
   
    # ikki sana orasidagi userga tegishli bolgan hisobotlarni yigindisi olish uchun
    user_month_hisobot = await  db.select_between_hisobot(user_id=2, sana1=sana1, sana2=sana2)
    print(user_month_hisobot) #

    # ikki sana orasidagi barcha userga tegishli bolgan hisobotlarni yigindisi olish uchun
    month_all_hisobot = await  db.select_all_between_hisobot(sana1=sana1, sana2=sana2)
    print(month_all_hisobot)  #


    # ikki sana orasidagi barcha userga tegishli bolgan hisobotlarni yigindisini userlar boyicha aloiha  olish uchun
    month_group_by_hisobot = await  db.select_group_by_between_hisobot(sana1=sana1, sana2=sana2)
    print(month_group_by_hisobot[3])  #


    # gaplashilgan mijozlar boyicha statistika
    st_gaplashilgan = await db.st_gaplashilgan()
    print(st_gaplashilgan) #typle of list qaytaradi

    # sotilgan mahsulotlar boyicha statistika
    st_sotilgan = await db.st_sotilgan()
    print(st_sotilgan)  #typle of list qaytaradi

    print('sassasasasasasasa')

    #haftalik hisobotlarni olish uchun
    today = date.today()
    weekday = today.weekday()
    bugun= date.today()
    year = today.year
    month = today.month
    hafta_boshi = date(year=2022, month=5, day=bugun.day-weekday)
    print(hafta_boshi)
    #haftalik_user_hisobot = await db.select_between_hisobot(user_id=3,sana1=hafta_boshi,sana2=bugun)
    #print(haftalik_user_hisobot)

asyncio.run(test())