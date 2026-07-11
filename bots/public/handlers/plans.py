from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.plan import Plan
from database.models.payment import Payment, PaymentStatus
from payments.client import create_pix_order
from core.utils import generate_qr_image
from bots.public.keyboards.main import main_menu

router = Router()

class BuyStates(StatesGroup):
    waiting_confirmation = State()

@router.callback_query(F.data == "show_plans")
async def show_plans(callback: CallbackQuery, db: AsyncSession):
    result = await db.execute(select(Plan))
    plans = result.scalars().all()

    if not plans:
        await callback.message.edit_text("Nenhum plano cadastrado no momento.")
        return

    text = "📋 <b>Catálogo de Planos</b>\n\n"
    kb = []

    for plan in plans:
        text += f"• <b>{plan.name}</b> - R$ {plan.price:.2f}\n{plan.description}\n\n"
        kb.append([InlineKeyboardButton(
            text=f"Comprar {plan.name} - R${plan.price}",
            callback_data=f"buy_plan_{plan.id}"
        )])

    kb.append([InlineKeyboardButton(text="↩️ Voltar", callback_data="main_menu")])

    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="HTML")
  @router.callback_query(F.data.startswith("buy_plan_"))
async def buy_plan(callback: CallbackQuery, db: AsyncSession, state: FSMContext):
    plan_id = int(callback.data.split("_")[-1])
    plan = await db.get(Plan, plan_id)

    if not plan:
        await callback.answer("Plano não encontrado!", show_alert=True)
        return

    payment, qr_text = await create_pix_order(db, callback.from_user.id, plan)

    if not payment:
        await callback.answer("Erro ao gerar pagamento. Tente novamente.", show_alert=True)
        return

    await state.update_data(payment_id=payment.id, plan_name=plan.name)

    text = f"""
✅ <b>Pagamento gerado com sucesso!</b>

Plano: <b>{plan.name}</b>
Valor: <b>R$ {plan.price:.2f}</b>

Escaneie o QR Code abaixo ou copie o código PIX.
O pagamento é automático via PIX.
"""

    qr_photo = generate_qr_image(qr_text)

    await callback.message.answer_photo(
        photo=qr_photo,
        caption=text,
        parse_mode="HTML"
    )

    await callback.message.answer(
        "Aguardando pagamento... Assim que confirmar, seu plano será liberado automaticamente.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Verificar Pagamento", callback_data=f"check_payment_{payment.id}")],
            [InlineKeyboardButton(text="↩️ Menu Principal", callback_data="main_menu")]
        ])
    )

    await state.set_state(BuyStates.waiting_confirmation)
  @router.callback_query(F.data.startswith("check_payment_"))
async def check_payment(callback: CallbackQuery, db: AsyncSession):
    payment_id = int(callback.data.split("_")[-1])
    payment = await db.get(Payment, payment_id)

    # Aqui você pode chamar a API do Mercado Pago para verificar status real
    # Por enquanto simulamos
    if payment and payment.status == PaymentStatus.APPROVED:
        await callback.answer("✅ Pagamento confirmado! Plano liberado.", show_alert=True)
        # Liberar acesso / enviar link / etc.
    else:
        await callback.answer("⏳ Pagamento ainda não confirmado. Aguarde ou tente novamente.", show_alert=True)
