import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db.models.users import UsersAddModel
from app.db.sessions import SessionDep
from app.schemas.users import UsersAddSchema, UsersSchema
from app.services import user_service

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

@router.get("/get_by_provider")
async def get_user_by_provider(session: SessionDep, provider: str, provider_id: str):
    user = await user_service.get_user_by_provider(session, provider, provider_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    u = UsersSchema.model_validate(user)
    logging.debug(f'get_user_by_provider {u}')
    return u