from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import DateTime, func, select
from project.reviews.models import Category, ReviewHistory
from project.reviews.schemas import CategoryTrend
from project.database import get_db
from datetime import datetime
from sqlalchemy.orm import Session
review_router = APIRouter(
    prefix="/reviews",
)

@review_router.get("/trends")
async def get_trends(db: AsyncSession = Depends(get_db)):
        # Subquery to get the latest review for each review_id
    # subquery = (
    #     select(
    #         ReviewHistory.review_id,
    #         func.max(ReviewHistory.id).label("latest_id")
    #     )
    #     .group_by(ReviewHistory.review_id)
    #     .subquery()
    # )
#     stmt = (
#     select(
#         Category.id,
#         Category.name,
#         Category.description,
#     )
    
# )

    #Adding category
    # cat = Category()
    # cat.name = "Bad"
    # cat.description = "This is a Bad category"
    # # cat.id = 2
    # # cat.reviews = "This is a very good store"
    # db.add(cat)
    # db.commit()
    # db.refresh(cat)
    # return cat

    # #Adding review History
    # hist = ReviewHistory()
    # hist.text = "This review 3"
    # hist.stars = 3
    # hist.review_id = "1525"
    # hist.tone = "Bad"
    # hist.sentiment = "Bad"
    # hist.category_id = 3
    # hist.created_at = datetime.now()
    # hist.updated_at = datetime.now()
    # db.add(hist)
    # db.commit()
    # db.refresh(hist)
    # return hist

    # Subquery to get the latest review for each review_id
    subquery = (
        select(
            ReviewHistory.review_id,
            func.max(ReviewHistory.id).label("latest_id")
        )
        .group_by(ReviewHistory.review_id)
        .subquery()
    )

        # Join the subquery with ReviewHistory to get the latest reviews
    latest_reviews = (
        select(ReviewHistory)
        .join(subquery, ReviewHistory.id == subquery.c.latest_id)
        .subquery()
    )

        # Calculate average stars and total reviews per category
    stmt = (
        select(
            Category.id,
            Category.name,
            Category.description,
            func.avg(latest_reviews.c.stars).label("average_stars"),
            func.count(latest_reviews.c.id).label("total_reviews")
        )
        .join(latest_reviews, Category.id == latest_reviews.c.category_id)
        .group_by(Category.id)
        .order_by(func.avg(latest_reviews.c.stars).desc())
        .limit(5)
    )
    result =  db.execute(stmt)
    categories = result.fetchall()


    # Transform results into the response model
    trends = [
        CategoryTrend(
            id=category.id,
            name=category.name,
            description=category.description,
            average_stars=category.average_stars,
            total_reviews=category.total_reviews
        )
        for category in categories
    ]
    print("SUbquery in /trends: ", categories)
    # Logic to retrieve users
    # return {"message": "GET Request for trends"}
    return trends

@review_router.get("/addReview")
def add_review(db: Session = Depends(get_db)):
    #Adding review History
    hist = ReviewHistory()
    hist.text = "This review 4"
    hist.stars = 2
    hist.review_id = "1"
    hist.tone = "Bad"
    hist.sentiment = "Bad"
    hist.category_id = 3
    hist.created_at = datetime.now()
    hist.updated_at = datetime.now()
    db.add(hist)
    db.commit()
    db.refresh(hist)
    return hist
    

@review_router.get("/")
async def get_reviews(category_id: int, cursor: Optional[datetime] = None, page_size: int = 15, db: Session = Depends(get_db)):
    query = db.query(ReviewHistory).filter(ReviewHistory.category_id == category_id)
    
    if cursor:
        query = query.filter(ReviewHistory.created_at < cursor)

    reviews = query.order_by(ReviewHistory.created_at.desc()).limit(page_size).all()

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")

    return reviews
    return {"message": "GEt request for get reviews", "category_id": category_id}

from . import models#  noqa
