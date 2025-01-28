from pydantic import BaseModel
from datetime import datetime

class CategoryTrend(BaseModel):
    id: int
    name: str
    description: str
    average_stars: float
    total_reviews: int


class ReviewResponse(BaseModel):
    id: int
    text: str
    stars: int
    review_id: str
    created_at: datetime
    tone: str
    sentiment: str
    category_id: int