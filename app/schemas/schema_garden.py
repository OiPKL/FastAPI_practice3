# schema_garden.py

from pydantic import BaseModel

class SensorUpdate(BaseModel):
    gardenTemp: float
    gardenHumid: float
    gardenWater: int

class GardenCreate(BaseModel):
    gardenTemp: float
    gardenHumid: float
    gardenWater: int
    gardenImage: str

class Garden(BaseModel):
    gardenTemp: float
    gardenHumid: float
    gardenWater: int
    gardenImage: str

    class Config:
        from_attributes = True