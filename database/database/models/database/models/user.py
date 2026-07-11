from sqlalchemy import Column, BigInteger, String, Boolean
from database.base import Base

class User(Base):
    __tablename__ = "users"
    
    telegram_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    username = Column(String, nullable=True)
    is_banned = Column(Boolean, default=False)
