# router_vegetable.py

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.database.model import User, Vegetable
from app.schemas.schema_user import UserCreate, User as UserPydantic
from app.schemas.schema_vegetable import VegetableCreate, Vegetable as VegetablePydantic
from typing import List, tuple
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

# SQLAlchemy 모델 (Vegetable, Vegetable) -> Pydantic 모델 (VegetablePydantic, VegetablePydantic)
def sqlalchemy_to_pydantic(vegetable: Vegetable) -> tuple[VegetablePydantic, VegetablePydantic]:
    temp_tuple_1 = VegetablePydantic(
        id=vegetable.id,
        vegetableName=vegetable.vegetableName,
        vegetableType=vegetable.vegetableType,
        vegetableChar=vegetable.vegetableChar,
        vegetableLevel=vegetable.vegetableLevel,
        vegetableDate=vegetable.vegetableDate,
        vegetableAge=vegetable.vegetableAge
    )

    temp_tuple_2 = VegetablePydantic(
        id=vegetable.id,
        vegetableName=vegetable.vegetableName,
        vegetableType=vegetable.vegetableType,
        vegetableChar=vegetable.vegetableChar,
        vegetableLevel=vegetable.vegetableLevel,
        vegetableDate=vegetable.vegetableDate,
        vegetableAge=vegetable.vegetableAge
    )

    return temp_tuple_1, temp_tuple_2

# 식물 등록 엔드포인트
@router.post("/api/me/plant", response_model=VegetablePydantic)
def register_plant(vegetable_data: VegetableCreate, db: Session = Depends(get_db)):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # 새로운 식물 생성 (고유 id는 자동으로 생성)
    new_vegetable = Vegetable(
        vegetableName=vegetable_data.vegetableName,
        vegetableType=vegetable_data.vegetableType,
        vegetableChar=vegetable_data.vegetableChar,
        vegetableDate=vegetable_data.vegetableDate,
        owner_id=current_user.id  # owner를 현재 사용자로 설정
    )
    
    # vegetableAge를 계산하고 업데이트
    new_vegetable.calculate_vegetable_age()

    db.add(new_vegetable)
    db.commit()
    db.refresh(new_vegetable)

    # User 모델의 ownedVegetableIDs에 추가
    temp_owned_ids = json.loads(current_user.ownedVegetableIDs)
    temp_owned_ids.append(new_vegetable.id)
    current_user.ownedVegetableIDs = json.dumps(temp_owned_ids)

    db.commit()
    db.refresh(current_user)
    
    return sqlalchemy_to_pydantic(new_vegetable)

# 식물 정보 엔드포인트
@router.get("/api/me/{vegetableID}", response_model=List[VegetablePydantic])
def get_owned_vegetable_by_id(vegetableID: int, db: Session = Depends(get_db)):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")

    if vegetableID not in json.loads(current_user.ownedVegetableIDs):
        raise HTTPException(status_code=404, detail="Vegetable not found")

    # 데이터베이스에서 vegetableID에 해당하는 정보 가져오기
    temp_vegetable_data = db.query(Vegetable).filter(Vegetable.id == vegetableID).first()

    if not temp_vegetable_data:
        raise HTTPException(status_code=404, detail="Vegetable not found")

    return [sqlalchemy_to_pydantic(temp_vegetable_data)]

# 식물 목록 엔드포인트 : 최대 두 개의 식물
@router.get("/api/me/ownedIDs", response_model=List[tuple[VegetablePydantic, VegetablePydantic]])
def get_owned_vegetables_by_id(db: Session = Depends(get_db)):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")

    # 사용자가 소유한 식물 ID 리스트 가져오기
    temp_redirect_2 = json.loads(current_user.ownedVegetableIDs)

    vegetables_data = []

    for vegetableID in temp_redirect_2[:2]:
        temp_vegetables_data = db.query(Vegetable).filter(Vegetable.id == vegetableID).first()
        
        if temp_vegetables_data:
            temp_pydantic = sqlalchemy_to_pydantic(temp_vegetables_data)
            vegetables_data.append({f'vegetableID_{vegetableID}': temp_pydantic})

    if len(temp_redirect_2) == 1:
        # 사용자가 가진 vegetableID가 하나일 때, 메인 화면 엔드포인트로 리다이렉트
        return RedirectResponse(url=f'/api/me/{temp_redirect_2[0]}')
    else:
        # 사용자가 가진 vegetableID가 두개일 때, 식물 목록 엔드포인트로 리다이렉트
        return tuple(vegetables_data)