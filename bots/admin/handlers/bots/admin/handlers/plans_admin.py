from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.plan import Plan

router = Router()

@router.message(Command("addplan"))
async def add_plan(message: Message, db: AsyncSession):
    # Exemplo simples - melhore com FSM para produção
    # Nome;Preço;Descrição
    try:
        _, name, price, desc = message.text.split(";", 3)
        plan = Plan(name=name.strip(), price=float(price), description=desc.strip())
        db.add(plan)
        await db.commit()
        await message.answer(f"✅ Plano '{name}' adicionado com sucesso!")
    except:
        await message.answer("❌ Formato incorreto.\nUso: /addplan Nome;Preco;Descricao")
