from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from config.settings import settings

router = Router()

@router.message(Command("start"))
async def admin_start(message: Message):
    if message.from_user.id != settings.ADMIN_TELEGRAM_ID:
        await message.answer("❌ Acesso negado.")
        return
    
    await message.answer(
        "👑 <b>Painel Administrativo</b>\n\n"
        "Comandos disponíveis:\n"
        "/planos - Gerenciar planos\n"
        "/usuarios - Ver usuários\n"
        "/broadcast - Enviar mensagem para todos\n"
        "/backup - Fazer backup do banco",
        parse_mode="HTML"
    )
