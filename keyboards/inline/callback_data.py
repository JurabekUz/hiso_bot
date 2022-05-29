from aiogram.utils.callback_data import CallbackData

auth_callback = CallbackData("auth", "item_name")
confirm_callback = CallbackData("submit", "item_name")
savollar_callback = CallbackData("savollar", "item_name")

create_callback = CallbackData("create", "action", "hisobot_id", "xodim_id")

oylar_callback = CallbackData('month','item_name')

select_callback = CallbackData('select', "name")