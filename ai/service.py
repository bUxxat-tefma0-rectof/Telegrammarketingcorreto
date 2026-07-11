from openai import AsyncOpenAI
from config.settings import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def get_ai_response(text: str, history: list = None):
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "system", "content": "Você é um assistente de vendas educado e útil."}] + (history or []),
            temperature=0.7
        )
        return response.choices[0].message.content
    except:
        return "Desculpe, não consegui responder. Vou transferir para o suporte humano."
