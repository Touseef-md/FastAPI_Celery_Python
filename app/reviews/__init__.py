from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from app.reviews.models import Category, ReviewHistory
from app.reviews.schemas import CategoryTrend
from app.database import get_db
from datetime import datetime
from sqlalchemy.orm import Session
from app.gemini import analyze_tone_and_sentiment
from . import models

review_router = APIRouter(
    prefix="/reviews",
)

@review_router.get("/trends")
async def get_trends(db: Session = Depends(get_db)):
    """
    Retrieve the top 5 categories with the highest average stars based on the latest reviews.

    Parameters:
    db (Session): The database session for asynchronous operations. This parameter is optional and defaults to Depends(get_db).

    Returns:
    List[CategoryTrend]: A list of CategoryTrend objects representing the top 5 categories with the highest average stars.
    """
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

    return trends

@review_router.get("/addReview")
def add_review(db: Session = Depends(get_db)):
    #Adding review History
    hist = ReviewHistory()
    hist.text = "This review 26"
    hist.stars = 3
    hist.review_id = "23"
    # hist.tone = "Bad"
    # hist.sentiment = "Bad"
    hist.category_id = 1
    hist.created_at = datetime.now()
    hist.updated_at = datetime.now()
    db.add(hist)
    db.commit()
    db.refresh(hist)
    return hist
    

@review_router.get("/")
async def get_reviews(category_id: int, cursor: Optional[datetime] = None, page_size: int = 15, db: Session = Depends(get_db)):
    """
    Retrieve a list of reviews for a specific category.

    Parameters:
    category_id (int): The ID of the category for which to retrieve reviews.
    cursor (Optional[datetime]): The cursor for pagination. If provided, only reviews created before this cursor will be returned.
    page_size (int): The number of reviews to return per page. Defaults to 15.
    db (Session): The database session for operations. This parameter is optional and defaults to Depends(get_db).

    Returns:
    List[ReviewHistory]: A list of ReviewHistory objects representing the retrieved reviews.

    Raises:
    HTTPException: If no reviews are found for the specified category.
    """
    query = db.query(ReviewHistory).filter(ReviewHistory.category_id == category_id)

    if cursor:
        query = query.filter(ReviewHistory.created_at < cursor)

    reviews = query.order_by(ReviewHistory.created_at.desc()).limit(page_size).all()

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")

    await update_reviews_with_analysis(reviews, db)
    return reviews

async def update_reviews_with_analysis(reviews : List[ReviewHistory], db: Session):

    for review in reviews:
        response = await analyze_tone_and_sentiment(review.text, review.stars)
        review.tone = response['tone']
        review.sentiment = response['sentiment']
        db.add(review)
    db.commit()