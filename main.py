import asyncio
import sys
from config.settings import settings

async def main():
    # Importar aqui para evitar problemas de importação circular
    from bots.public.main import main as public_bot
    from bots.admin.main import main as admin_bot
    from payments.webhook_server import app as webhook_app
    
    print("🚀 Iniciando sistema completo...")

    # Rodar os bots e webhook juntos
    tasks = [
        asyncio.create_task(public_bot()),
        asyncio.create_task(admin_bot()),
    ]
    
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())
