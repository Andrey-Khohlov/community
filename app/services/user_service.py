import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.users import  UsersAddModel
from app.db.sessions import SessionDep

logging.basicConfig(level=logging.DEBUG)

async def get_user_by_provider(session: SessionDep, provider: str, provider_id: str):
    """
    Находит пользователя по провайдеру и ID провайдера
    """
    result = await session.execute(
        select(UsersAddModel).where(
            UsersAddModel.provider == str(provider),
            UsersAddModel.provider_id == str(provider_id)
        )
    )
    r = result.scalar()
    logging.debug(f'get_user_by_provider {r}')
    return r
