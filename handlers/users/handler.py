from aiogram import types

from loader import dp
from states.states import *
from data.config import ADMINS

@dp.message_handler(state=HisobotState.all_states,user_id=ADMINS)
async def bot_echo(message: types.Message):
    await message.answer("Botdan to'g'ri foydalaning, amalni davom etiring")


@dp.message_handler(commands=['oylik','haftalik','kunlik','allusers'],state=HisobotState.all_states)
async def bot_echo(message: types.Message):
    await message.answer("Bu buyruqlar adminlar uchun. Iltimos Botdan to'gri foydalaning\n Amalni davom ettiring")

