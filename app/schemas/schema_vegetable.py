# schema_vegetable.py

from pydantic import BaseModel, Field
from enum import Enum

# 사용 가능한 Type 선택지 정의
class VegetableType(str, Enum):
    Lettuce = "Lettuce"
    Sesame = "Sesame"
    Pepper = "Pepper"
    Tomato = "Tomato"

# 사용 가능한 Char 선택지 정의
class VegetableChar(str, Enum):
    PokemonA = "PokemonA"
    PokemonB = "PokemonB"
    PokemonC = "PokemonC"
    PokemonD = "PokemonD"

class VegetableCreate(BaseModel):
    vegetableName: str
    vegetableType: VegetableType = Field(..., description="Type 선택: Lettuce, Sesame, Pepper, Tomato")
    vegetableChar: VegetableChar = Field(..., description="Char 선택: PokemonA, PokemonB, PokemonC, PokemonD")
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
