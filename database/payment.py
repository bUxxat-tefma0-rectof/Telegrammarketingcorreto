from database.base import Base
from sqlalchemy import Column, Integer, BigInteger, String, Float, Enum
import enum

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    mp_payment_id = Column(String)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    amount = Column(Float)
    status = Column(String, default=PaymentStatus.PENDING)
    qr_code = Column(Text)
    qr_text = Column(Text)
