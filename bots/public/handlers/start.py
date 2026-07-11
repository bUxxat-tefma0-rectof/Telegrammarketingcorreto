from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.models.user import User
from bots.public.keyboards.main import main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, db):
    user = await db.get(User, message.from_user.id)
    if not user:
        user = User(
            telegram_id=message.from_user.id,
            name=message.from_user.full_name,
            username=message.from_user.username
        )
        db.add(user)
        await db.commit()

    await message.answer(
        f"👋 Olá <b>{message.from_user.full_name}</b>!\n\n"
        "Bem-vindo à plataforma de planos e serviços.\n"
        "Escolha uma opção abaixo:",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )
