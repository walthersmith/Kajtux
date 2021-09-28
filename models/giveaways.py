from sqlalchemy import Integer, Column, String, BigInteger, Text, DateTime, TIMESTAMP, ForeignKey
from models.base import Base

class Giveaways(Base):
    __tablename__  ='giveaway'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    worth = Column(BigInteger, nullable=True)
    thumbnail = Column(Text,nullable=True)
    image = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    instructions = Column(String(255), nullable=True)
    open_giveaway_url = Column(String(255), nullable=True)
    published_date = Column(DateTime, nullable=True)
    type = Column(String(255), nullable=True)
    platforms = Column(String(255), nullable=True)
    end_date = Column(DateTime, nullable=True)
    users = Column(Integer, nullable=True)
    status = Column(String(255), nullable=True)
    game_power_url = Column(String(255), nullable=True)
    open_giveaway= Column(String(255), nullable=True)

    def __init__(self, id, title, worth, thumbnail, image, description, instructions,open_giveaway_url,published_date,
                 type,platforms,end_date,users,status,game_power_url, open_giveaway):
        self.id = id
        self.title = title
        self.worth = worth
        self.thumbnail = thumbnail
        self.image = image
        self.description = description
        self.instructions = instructions
        self.open_giveaway_url = open_giveaway_url
        self.published_date = published_date
        self.type = type
        self.platforms = platforms
        self.end_date = end_date
        self.users = users
        self.status = status
        self.game_power_url = game_power_url
        self.open_giveaway = open_giveaway