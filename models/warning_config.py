from sqlalchemy import Integer, Column, String, BigInteger, TIMESTAMP, ForeignKey, func
from models.base import  Base
from sqlalchemy.orm import relationship

from models.guilds import Guilds


class Warning_config(Base):
    __tablename__ = 'warning_config'

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'))
    guild = relationship(Guilds)
    limit = Column(Integer, nullable=True)
    jail_role = Column(BigInteger, nullable=True)
    jail_time = Column(Integer, nullable=True)
    voice_ch_id = Column(BigInteger, nullable=True)
    text_ch_id = Column(BigInteger, nullable=True)
    timestamp = Column(TIMESTAMP, server_default=func.now())

    def __str__(self):
        return f"guild_id : {self.guild_id}"