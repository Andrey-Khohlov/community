import logging

from fastapi import APIRouter
from sqlalchemy import select

from app.db.models.users import UsersAddModel
from app.db.sessions import SessionDep
from app.schemas.users import UsersAddSchema


# logging.basicConfig(level=logging.DEBUG)

router = APIRouter()

@router.post("/")
async def add_user(user: UsersAddSchema, session: SessionDep):
    new_user = UsersAddModel(**user.model_dump())
    logging.debug('add_user', new_user)
    session.add(new_user)
    await session.commit()
    return {"Ok": True}

@router.get("/")
async def get_user(session: SessionDep):
    query = select(UsersAddModel)
    user = await session.execute(query)
    return {"Ok": user.scalars().all()}