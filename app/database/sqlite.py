# sqlite.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

DATABASE_URL = "sqlite:///./test.sqlite"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    from app.database.model import Base
    Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    return db