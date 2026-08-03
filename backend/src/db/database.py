from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = sessionmaker(bind=engine) if engine else None
Base = declarative_base()

def get_db():
    if not SessionLocal:
        raise RuntimeError('DATABASE_URL not set')
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
