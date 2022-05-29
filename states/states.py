from aiogram.dispatcher.filters.state import StatesGroup, State

class DateState(StatesGroup):
    days = State()
    week = State()
    month = State()
    xodim_oy = State()
    xodim_kun = State()


class AuthState(StatesGroup):
    password = State()
    login = State()
    logined = State()

class RegisterState(StatesGroup):
    password = State()
    name = State()
    sure_name = State()
    birthday = State()
    contact = State()
    confirm = State()

class HisobotState(StatesGroup):
    zayafka = State()
    gaplashilgan = State()
    sotilgan = State()
    tel_tushmagan = State()
    xato_nomer = State()
    berma_adash = State()
    otkaz = State()
    naqt = State()
    click = State()
    boshqacha_tolov = State()
    maxsus_narx = State()
    ehson = State()
    sotilgan2 = State()
    mijozlar = State()
    summa = State()
    tasdiqlash = State()
    qayta_kirit = State()



