from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("oylik", "oylik hisobotlar"),
            types.BotCommand("haftalik", "haftalik hisobotlar"),
            types.BotCommand("kunlik", "kunlik hisobotlar"),
            types.BotCommand("allusers", 'Xodimlar'),
            types.BotCommand("profil", 'Bosh Menu')
        ]
    )
