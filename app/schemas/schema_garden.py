# schema_garden.py

from pydantic import BaseModel

class GardenUpdate(BaseModel):
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

    class Config:
        from_attributes = True