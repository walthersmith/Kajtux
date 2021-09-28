from sqlalchemy import Integer, Column, BigInteger, DateTime, TIMESTAMP, ForeignKey, func
from .base import Base
from sqlalchemy.orm import relationship

from .guilds import Guilds
from .users import Users


class Jail(Base):
    __tablename__ = 'jail'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    user = relationship(Users)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'))
    guild = relationship(Guilds)
    end_date = Column(DateTime, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=False,server_default=func.now())

