from sqlalchemy import Integer, Column, BigInteger, TIMESTAMP, ForeignKey, func, String
from sqlalchemy.orm import relationship

from models.base import Base
from models.guilds import Guilds
from models.users import Users


class Users_roles(Base):
    __tablename__ = 'users_roles'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    users = relationship(Users)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'))
    guild = relationship(Guilds)
    id_role = Column(BigInteger, nullable=False)
    role_name = Column(String(255), nullable=True)
    timestamp = Column(TIMESTAMP,server_default=func.now())
