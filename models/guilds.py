from sqlalchemy import Integer, Column, String, TIMESTAMP, func, BigInteger
from models.base import Base


class Guilds(Base):
    __tablename__ = 'guilds'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255),nullable=True)
    timestamp = Column(TIMESTAMP, server_default=func.now())
