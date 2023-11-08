# model.py

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.sqlite import Base
from datetime import datetime
import json

class User(Base):
    __tablename__ = "UserID"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    age = Column(Integer)
    # 저장은 JSON 문자열, 읽기쓰기는 Python 배열
    ownedVegetableIDs = Column(String, default="[]", server_default="[]")
    login_time = Column(DateTime, default=datetime.utcnow)

class Vegetable(Base):
    __tablename__ = "VegetableID"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    vegetableName = Column(String)
    vegetableType = Column(String)
    vegetableChar = Column(String)
    vegetableLevel = Column(Integer, default=2)
    vegetableDate = Column(String)
    vegetableAge = Column(Integer)
    owner_id = Column(Integer, ForeignKey("UserID.id"))

    def calculate_vegetable_age(self):
        if self.vegetableDate:
            temp_vegetable_date = datetime.strptime(self.vegetableDate, "%Y-%m-%d")
            vegetable_month = temp_vegetable_date.month
            vegetable_date = temp_vegetable_date.date()

            temp_current_date = datetime.utcnow()
            current_month = temp_current_date.month
            current_date = temp_current_date.date()

            if vegetable_month == current_month:
                vegetable_age = (current_date - vegetable_date).days
            else:
                if vegetable_month < current_month:
                    if vegetable_month == 10 and current_month == 11:
                        vegetable_age = (31 - vegetable_date.day) + current_date.day
                    elif vegetable_month == 11 and current_month == 12:
                        vegetable_age = (30 - vegetable_date.day) + current_date.day
                    elif vegetable_month == 10 and current_month == 12:
                        vegetable_age = (31 - vegetable_date.day) + 30 + current_date.day
                    else:
                        vegetable_age = 0
                else:
                    vegetable_age = 0

            if vegetable_age >= 0:
                self.vegetableAge = vegetable_age

class Garden(Base):
    __tablename__ = "MyGarden"
    id = Column(Integer, primary_key=True, index=True)
    gardenTemp = Column(Float)
    gardenHumid = Column(Float)
    gardenWater = Column(Integer)
    gardenImage = Column(String)