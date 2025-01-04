from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.models import Model
from app.db.models.users import UsersAddModel
from app.db.sessions import engine, SessionDep, get_session, new_async_session


async def setup_database():
    engine.echo = False
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
        await conn.run_sync(Model.metadata.create_all)
    engine.echo = True
    return {"DB has been created": True}


async def insert_init_data():
    async with new_async_session() as session:
        user1 = UsersAddModel(username="admin", email="admin", password="admin", created_at="2022-01-01 00:00:00")
        user2 = UsersAddModel(username="user", email="user", password="user", created_at="2022-01-01 00:00:00")
        session.add_all([user1, user2])
        await session.commit()
    return {"Data has been inserted": True}
