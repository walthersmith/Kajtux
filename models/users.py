from sqlalchemy import Integer, Column, String, BigInteger, Text, DateTime, TIMESTAMP, ForeignKey, func
from models.base import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(25),nullable=True)
    timestamp = Column(TIMESTAMP,server_default=func.now())
