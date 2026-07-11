from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from ai.service import get_ai_response
from config.settings import settings

router = Router()

class SupportStates(StatesGroup):
    waiting_message = State()

@router.callback_query(F.data == "support")
async def start_support(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🧠 <b>Suporte com IA</b>\n\n"
        "Digite sua dúvida ou pergunta. Se a IA não conseguir responder, será encaminhado para suporte humano.",
        parse_mode="HTML"
    )
    await state.set_state(SupportStates.waiting_message)

@router.message(SupportStates.waiting_message)
async def handle_support_message(message: Message, state: FSMContext):
    response = await get_ai_response(message.text)
    
    if "suporte humano" in response.lower() or len(response) < 30:
        await message.answer("🔄 Transferindo para suporte humano...")
        # Aqui você pode enviar mensagem para o admin
        await message.bot.send_message(
            settings.ADMIN_TELEGRAM_ID,
            f"❗ Novo pedido de suporte de {message.from_user.full_name} (ID: {message.from_user.id}):\n\n{message.text}"
        )
    else:
        await message.answer(response)
    
    await state.clear()
