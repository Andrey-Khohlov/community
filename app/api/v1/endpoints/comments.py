from fastapi import APIRouter
from sqlalchemy import select

from app.db.sessions import SessionDep
from app.db.models.comments import CommentsAddModel
from app.schemas.comments import CommentsAddSchema

router = APIRouter()

@router.post("/comments")
async def add_comment(comment: CommentsAddSchema, session: SessionDep):
    new_comment = CommentsAddModel(**comment.model_dump())
    session.add(new_comment)
    await session.commit()
    return {"Ok": True}

@router.get("/comments")
async def get_comment(session: SessionDep):
    query = select(CommentsAddModel)
    comment = await session.execute(query)
    return {"Ok": comment.scalars().all()}