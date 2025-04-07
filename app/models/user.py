from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)


class UserActivity(Base):
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="activities")


User.activities = relationship("UserActivity", back_populates="user")
