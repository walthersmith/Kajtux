from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, BigInteger
from sqlalchemy.orm import relationship

from models.guilds import Guilds
from models.base import Base
from models.users import Users


class Users_warnings(Base):
    __tablename__ = 'user_warnings'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger ,ForeignKey('users.id'))
    user = relationship(Users)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'))
    guild = relationship(Guilds)
    warnings = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())


