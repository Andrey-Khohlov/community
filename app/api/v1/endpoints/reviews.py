from fastapi import APIRouter
from sqlalchemy import select

from app.db.models.reviews import ReviewsAddModel
from app.db.sessions import SessionDep
from app.schemas.reviews import ReviewsAddSchema

router = APIRouter()


@router.post("/")
async def add_review(review: ReviewsAddSchema, session: SessionDep):
    new_review = ReviewsAddModel(**review.model_dump())
    session.add(new_review)
    await session.commit()
    return {"Ok": True}


@router.get("/")
async def get_review(session: SessionDep):
    query = select(ReviewsAddModel)
    review = await session.execute(query)
    return {"Ok": review.scalars().all()}