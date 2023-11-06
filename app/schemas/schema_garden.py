# schema_garden.py

from pydantic import BaseModel

class GardenCreate(BaseModel):
    gardenTemp: float
    gardenHumid: float
    gardenWater: int
    gardenImage: bytes

class Garden(BaseModel):
    id: int
    gardenTemp: float
    gardenHumid: float
    gardenWater: int
    gardenImage: bytes