# router_user.py

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.database.model import User
from app.schemas.schema_user import UserCreate, User as UserPydantic
from app.routers import router_vegetable
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

    db_user = User(
        username=user.username,
        password=user.password,
        name=user.name,
        age=user.age,
        )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return sqlalchemy_to_pydantic(db_user)

# 로그인 엔드포인트
@router.post("/login", response_model=UserPydantic)
def login_user(username: str, password: str, db: Session = Depends(get_db)):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).filter(User.username == username).first()

    if current_user is None or current_user.password != password:
        raise HTTPException(status_code=401, detail="Login failed")
    
    current_user.login_time = datetime.utcnow()
    db.commit()

    return sqlalchemy_to_pydantic(current_user)

# 사용자 엔드포인트 : Redirect 처리
@router.get("/me", response_model=UserPydantic)
def get_current_user(db: Session = Depends(get_db)
    # , redirect: bool = Query(True, description="Automatically redirect based on ownedVegetableIDs")
    ):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # if redirect:
    #     temp_redirect = json.loads(current_user.ownedVegetableIDs)
    
    #     if not temp_redirect:
    #         # 사용자가 가진 vegetableID가 없을 때, 식물 등록 엔드포인트로 리다이렉트
    #         return RedirectResponse(url='/me/plant')
    #     elif len(temp_redirect) == 1:
    #         # 사용자가 가진 vegetableID가 하나일 때, 메인 화면 엔드포인트로 리다이렉트
    #         return RedirectResponse(url=f'/me/{temp_redirect[0]}')
    #     else:
    #         # 사용자가 가진 vegetableID가 두개일 때, 식물 목록 엔드포인트로 리다이렉트
    #         return RedirectResponse(url='/me/ownedIDs') 

    return sqlalchemy_to_pydantic(current_user)