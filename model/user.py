from sqlalchemy import Column, String, Integer

from model import role
from model.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegramId = Column(Integer)
    userName = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    languageCode = Column(String)
    userRole = Column(String)
    subgroup = Column(Integer)

    def __init__(self, message):
        self.telegramId = message.from_user.id
        self.userName = message.from_user.username
        self.firstName = message.from_user.first_name
        self.lastName = message.from_user.last_name
        self.languageCode = message.from_user.language_code
        self.userRole = role.Role.user.name


