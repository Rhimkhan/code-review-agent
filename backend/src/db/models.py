from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from datetime import datetime
from src.db.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    github_username = Column(String, unique=True)
    email = Column(String, unique=True)
    api_calls_today = Column(Integer, default=0)
    daily_limit = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)

class ReviewHistory(Base):
    __tablename__ = 'review_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    repo = Column(String)
    pr_number = Column(Integer)
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
