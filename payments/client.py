import mercadopago
from config.settings import settings
from database.models.payment import Payment
from sqlalchemy.ext.asyncio import AsyncSession

sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

async def create_pix_order(db: AsyncSession, user_id: int, plan):
    payment_data = {
        "transaction_amount": plan.price,
        "description": f"Compra de {plan.name}",
        "payment_method_id": "pix",
        "payer": {"email": f"user{user_id}@example.com"}
    }

    result = sdk.payment().create(payment_data)

    if result['status'] == 201:
        qr = result['point_of_interaction']['transaction_data']
        payment = Payment(
            mp_payment_id=str(result['id']),
            user_id=user_id,
            plan_id=plan.id,
            amount=plan.price,
            qr_code=qr.get('qr_code_base64'),
            qr_text=qr.get('qr_code')
        )
        db.add(payment)
        await db.commit()
        return payment, qr['qr_code']
    return None, None
