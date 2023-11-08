# schema_vegetable.py

from pydantic import BaseModel, Field
from enum import Enum

# 사용 가능한 Type 선택지 정의
class VegetableType(str, Enum):
    TypeA = "TypeA"
    TypeB = "TypeB"
    TypeC = "TypeC"
    TypeD = "TypeD"

# 사용 가능한 Char 선택지 정의
class VegetableChar(str, Enum):
    CharA = "CharA"
    CharB = "CharB"
    CharC = "CharC"
    CharD = "CharD"

class VegetableCreate(BaseModel):
    vegetableName: str
    vegetableType: VegetableType = Field(..., description="Type 선택: TypeA, TypeB, TypeC, TypeD")
    vegetableChar: VegetableChar = Field(..., description="Char 선택: CharA, CharB, CharC, CharD")
    vegetableDate: str

class Vegetable(BaseModel):
    id: int
    vegetableName: str
    vegetableType: VegetableType
    vegetableChar: VegetableChar
    vegetableLevel: int
    vegetableDate: str
    vegetableAge: int

    class Config:
        from_attributes = True
