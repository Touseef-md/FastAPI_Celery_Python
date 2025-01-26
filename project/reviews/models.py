# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from project.database import Base, engine
from datetime import datetime

print("Review model  file called")
class Category(Base):
    print("Class category called")
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String, nullable=True)

    reviews = relationship("ReviewHistory", back_populates="category")

class ReviewHistory(Base):
    print("Class reviewHIstory called")
    __tablename__ = 'review_history'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=True)
    stars = Column(Integer, nullable=False)
    review_id = Column(String(255), nullable=False)
    tone = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="reviews")

class AccessLog(Base):
    __tablename__ = 'access_logs'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

Base.metadata.create_all(engine)