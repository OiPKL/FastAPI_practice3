# router_user.py

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.database.model import User
from app.schemas.schema_user import UserCreate, User as UserPydantic
from datetime import datetime
import json

router = APIRouter()

# SQLAlchemy 모델 (User) -> Pydantic 모델 (UserPydantic)
def sqlalchemy_to_pydantic(user: User) -> UserPydantic:

    return UserPydantic(
        username=user.username,
        name=user.name,
        age=user.age,
        ownedVegetableId=json.loads(user.ownedVegetableIDs)
    )

# 회원가입 엔드포인트
@router.post("/register", response_model=UserPydantic)
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        password=user.password,
        name=user.name,
        age=user.age,
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return sqlalchemy_to_pydantic(new_user)

# 로그인 엔드포인트
@router.post("/login", response_model=UserPydantic)
def login_user(username: str, password: str, db: Session = Depends(get_db)):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).filter(User.username == username).first()

    if current_user is None or current_user.password != password:
        raise HTTPException(status_code=401, detail="Login failed")
    
    current_user.login_time = datetime.utcnow()

    db.commit()
    db.refresh(current_user)

    return sqlalchemy_to_pydantic(current_user)

# 사용자 정보 엔드포인트
@router.get("/me", response_model=UserPydantic)
def get_current_user(db: Session = Depends(get_db)):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")

    db.refresh(current_user)
    owned_vegetable_ids = json.loads(current_user.ownedVegetableIDs)
    current_user.ownedVegetableIDs = owned_vegetable_ids
    db.refresh(current_user)

    return sqlalchemy_to_pydantic(current_user)