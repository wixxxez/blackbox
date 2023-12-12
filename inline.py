from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

briefcase = "&#128187" , ParseMode.HTML

def log_inline():
    builder = InlineKeyboardBuilder
    builder.button(text = f"{briefcase}Загрузить логи{briefcase}", callback_data= "1")

