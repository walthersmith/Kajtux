from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from models.base import Base
from models.guilds import Guilds
from models.users import Users


class Warning_log(Base):
    __tablename__ = 'warning_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    user = relationship(Users)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'))
    guild = relationship(Guilds)
    reason = Column(String(255), nullable=True)
    timestamp = Column(TIMESTAMP, server_default=func.now())

    def __init__(self):
        pass
