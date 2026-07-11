from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = [
        [InlineKeyboardButton(text="🛒 Ver Planos", callback_data="show_plans")],
        [InlineKeyboardButton(text="📋 Meus Planos", callback_data="my_plans")],
        [InlineKeyboardButton(text="❓ Suporte / Dúvidas", callback_data="support")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
