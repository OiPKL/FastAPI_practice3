# schema_user.py

from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    age: int

class User(BaseModel):
    username: str
    name: str
    age: int

    class Config:
        from_attributes = True