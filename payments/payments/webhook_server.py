from fastapi import FastAPI, Request, HTTPException
from config.settings import settings

app = FastAPI()

@app.post("/webhook")
async def mercadopago_webhook(request: Request):
    data = await request.json()
    # Processar atualização de pagamento, atualizar BD, liberar acesso
    print("Webhook recebido:", data)
    return {"status": "ok"}
