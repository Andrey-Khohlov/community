from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db.sessions import SessionDep
from app.schemas.comments import CommentsAddSchema
from app.db.models.coffees import CoffeesAddModel
from app.db.models.comments import CommentsAddModel



router = APIRouter()

@router.post("/")
async def add_comment(comment: CommentsAddSchema, session: SessionDep):
    new_comment = CommentsAddModel(**comment.model_dump())
    session.add(new_comment)
    await session.commit()
    return {"Ok": True}

@router.get("/{coffee_id}")
async def get_comment(session: SessionDep, coffee_id: int):
    query = (select(CommentsAddModel)
             .filter(CommentsAddModel.product_id == coffee_id)
             .options(joinedload(CommentsAddModel.user))  # Жадная загрузка пользователя
             .order_by(CommentsAddModel.created_at)
             )
    query_coffee = select(CoffeesAddModel).filter(CoffeesAddModel.id == coffee_id)
    comment = await session.execute(query)
    coffee = await session.execute(query_coffee)
    return {"Ok": comment.scalars().all(), "coffee": coffee.scalars().one_or_none()}