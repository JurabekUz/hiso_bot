from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from keyboards.default.services_board import services_menu
from loader import dp

from keyboards.inline.menu_boards import auth_menu
from states.states import AuthState


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Salom, {message.from_user.full_name}!",reply_markup=auth_menu)

@dp.message_handler(commands='profil', state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    msg = "<b>Shaxsiy Profil</b> \n📋 Hisobot topshirish \n⚙️Sozlash \n📈 Statistika"
    await message.answer(msg, reply_markup=services_menu)
    await AuthState.logined.set()

@dp.message_handler()
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!"
                         "Iltimos Profilingizga kiring yoki Ro'yxatdan o'ting",reply_markup=auth_menu)

