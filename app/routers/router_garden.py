# router_garden.py

from fastapi import File, UploadFile, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.database.model import Garden
from app.schemas.schema_garden import SensorUpdate, GardenCreate, Garden as GardenPydantic

router = APIRouter()

# SQLAlchemy 모델 (Garden) -> Pydantic 모델 (GardenPydantic)
def sqlalchemy_to_pydantic(garden: Garden) -> GardenPydantic:

    return GardenPydantic(
        gardenTemp=garden.gardenTemp,
        gardenHumid=garden.gardenHumid,
        gardenWater=garden.gardenWater,
        gardenImage=garden.gardenImage
    )

# 텃밭 센서 엔드포인트
@router.put("/sensor", response_model=GardenPydantic)
def update_sensor_data(sensor_update: SensorUpdate, db: Session = Depends(get_db)):

    new_sensor = db.query(Garden).get(1)

    if not new_sensor:
        raise HTTPException(status_code=404, detail="Garden data not found")
    
    new_sensor.gardenTemp = sensor_update.gardenTemp
    new_sensor.gardenHumid = sensor_update.gardenHumid
    new_sensor.gardenWater = sensor_update.gardenWater

    db.commit()
    db.refresh(new_sensor)

    return sqlalchemy_to_pydantic(new_sensor)

# 텃밭 이미지 엔드포인트
@router.put("/image", response_model=GardenPydantic)
def update_garden_image(file: UploadFile = File(...), db: Session = Depends(get_db)):

    new_image = db.query(Garden).get(1)

    if not new_image:
        raise HTTPException(status_code=404, detail="Garden data not found")

    # 파일을 서버 폴더에 저장
    with open(f"app/database/garden_images/{file.filename}", "wb") as image_file:
        image_file.write(file.file.read())

    # 이미지 경로를 DB에 저장
    new_image.gardenImage = f"app/database/{file.filename}"

    db.commit()
    db.refresh(new_image)

    return sqlalchemy_to_pydantic(new_image)

# 기본 텃밭 엔드포인트
@router.post("/mygarden", response_model=GardenPydantic)
def create_garden(my_garden: GardenCreate = GardenCreate(
        gardenTemp=25.0,
        gardenHumid=50.0,
        gardenWater=60,
        gardenImage="app/database/default_image.png"),  # 이미지 파일 경로를 저장
        db: Session = Depends(get_db)):

    default_garden = Garden(
        gardenTemp=my_garden.gardenTemp,
        gardenHumid=my_garden.gardenHumid,
        gardenWater=my_garden.gardenWater,
        gardenImage=my_garden.gardenImage
    )

    db.add(default_garden)
    db.commit()
    db.refresh(default_garden)

    return sqlalchemy_to_pydantic(default_garden)

# 텃밭 정보 엔드포인트
@router.get("/mygarden", response_model=GardenPydantic)
def get_garden_data(db: Session = Depends(get_db)):

    garden_data = db.query(Garden).get(1)

    if not garden_data:
        raise HTTPException(status_code=404, detail="Garden data not found")

    db.refresh(garden_data)

    return GardenPydantic(
        gardenTemp=garden_data.gardenTemp,
        gardenHumid=garden_data.gardenHumid,
        gardenWater=garden_data.gardenWater,
        gardenImage=garden_data.gardenImage  # 이미지 파일 경로를 반환
    )