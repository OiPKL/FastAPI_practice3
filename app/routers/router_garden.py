# router_garden.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.database.model import Garden
from app.schemas.schema_garden import GardenUpdate, Garden as GardenPydantic
from typing import List

router = APIRouter()

# SQLAlchemy 모델 (Garden) -> Pydantic 모델 (GardenPydantic)
def sqlalchemy_to_pydantic(garden: Garden) -> GardenPydantic:

    return GardenPydantic(
        id=garden.id,
        gardenTemp=garden.gardenTemp,
        gardenHumid=garden.gardenHumid,
        gardenWater=garden.gardenWater,
        gardenImage=garden.gardenImage
    )

# 텃밭 업데이트 엔드포인트
@router.post("/garden", response_model=GardenPydantic)
def update_garden_data(garden: GardenUpdate, db: Session = Depends(get_db)):

    db_garden = Garden(**garden.dict())
    db.add(db_garden)
    db.commit()
    db.refresh(db_garden)

    return sqlalchemy_to_pydantic(db_garden)

# 텃밭 정보 엔드포인트
@router.get("/mygarden", response_model=List[GardenPydantic])
def get_garden_data(db: Session = Depends(get_db)):

    temp_garden_data = db.query(Garden).first()

    if not temp_garden_data:
        raise HTTPException(status_code=404, detail="Garden data not found")

    return sqlalchemy_to_pydantic(temp_garden_data)