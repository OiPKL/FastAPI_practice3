# router_vegetable.py

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.database.model import User, Vegetable
from app.schemas.schema_vegetable import VegetableCreate, Vegetable as VegetablePydantic
import json

router = APIRouter()

# SQLAlchemy 모델 (Vegetable) -> Pydantic 모델 (VegetablePydantic)
def sqlalchemy_to_pydantic(vegetable: Vegetable) -> VegetablePydantic:

    return VegetablePydantic(
        id=vegetable.id,
        vegetableName=vegetable.vegetableName,
        vegetableType=vegetable.vegetableType,
        vegetableChar=vegetable.vegetableChar,
        vegetableLevel=vegetable.vegetableLevel,
        vegetableDate=vegetable.vegetableDate,
        vegetableAge=vegetable.vegetableAge
    )

# 식물 등록 엔드포인트
@router.post("/me/plant", response_model=VegetablePydantic)
def register_plant(vegetable_data: VegetableCreate, db: Session = Depends(get_db)):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")

    new_vegetable = Vegetable(
        vegetableName=vegetable_data.vegetableName,
        vegetableType=vegetable_data.vegetableType,
        vegetableChar=vegetable_data.vegetableChar,
        vegetableDate=vegetable_data.vegetableDate,
        owner_id=current_user.id  # owner를 현재 사용자로 설정
    )

    new_vegetable.calculate_vegetable_age()

    db.add(new_vegetable)
    db.commit()
    db.refresh(new_vegetable)

    # User 모델의 ownedVegetableIDs에 추가
    new_ownedIDs = json.loads(current_user.ownedVegetableIDs)
    new_ownedIDs.append(new_vegetable.id)
    current_user.ownedVegetableIDs = json.dumps(new_ownedIDs)

    db.commit()
    db.refresh(current_user)

    return sqlalchemy_to_pydantic(new_vegetable)

# 식물 정보 엔드포인트
@router.get("/me/{vegetableID}", response_model=VegetablePydantic)
def get_owned_vegetable_by_id(vegetableID: int, db: Session = Depends(get_db)):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")

    if vegetableID not in json.loads(current_user.ownedVegetableIDs):
        raise HTTPException(status_code=404, detail="Vegetable not found")

    vegetableID_data = db.query(Vegetable).filter(Vegetable.id == vegetableID).first()

    if not vegetableID_data:
        raise HTTPException(status_code=404, detail="Vegetable not found")
    
    db.refresh(vegetableID_data)
    
    return sqlalchemy_to_pydantic(vegetableID_data)