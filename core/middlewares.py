from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import AsyncSessionLocal
from database.models.user import User

class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with AsyncSessionLocal() as session:
            data["db"] = session
            result = await handler(event, data)
            await session.commit()
            return result

class BanMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message | CallbackQuery, data):
        db: AsyncSession = data.get("db")
        user_id = event.from_user.id
        
        user = await db.get(User, user_id)
        if user and user.is_banned:
            if isinstance(event, Message):
                await event.answer("Você foi banido do sistema.")
            return
        
        return await handler(event, data)
