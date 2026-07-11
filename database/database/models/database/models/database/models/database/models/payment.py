from sqlalchemy import Column, Integer, BigInteger, String, Float
from database.base import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mp_payment_id = Column(String)
    user_id = Column(BigInteger)
    plan_id = Column(Integer)
    amount = Column(Float)
    status = Column(String, default="pending")
    qr_code = Column(Text)
    qr_text = Column(Text)
