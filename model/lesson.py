from sqlalchemy import Column, Integer, String, Time

from model.base import Base


class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    startTime = Column(Time)
    endTime = Column(Time)
    teacher = Column(String)
    place = Column(String)
    day = Column(String)
    subgroup = Column(Integer)

    def __init__(self, name, startTime, endTime, teacher, place, subgroup, day):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.teacher = teacher
        self.place = place
        self.subgroup = subgroup
        self.day = day
