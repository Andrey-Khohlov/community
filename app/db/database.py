import asyncio
from typing import Annotated

from sqlalchemy import String, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# sync_engine = create_engine(
#     url=settings.DATABASE_URL_psycopg,
#     echo=True,
#     # pool_size=5,
#     # max_overflow=10,
# )
#
# async_engine = create_async_engine(
#     url=settings.DATABASE_URL_asyncpg,
#     echo=True,
#     # pool_size=5,
#     # max_overflow=10,
# )

# with sync_engine.connect() as conn:
#     res = conn.execute(text("SELECT VERSION()"))
#     print(f"{res.all()=}")
#
# async def get_123():
#     async with async_engine.begin() as conn:
#         res = await conn.execute(text("SELECT VERSION()"))
#         print(f"{res.all()=}")
# asyncio.run(get_123())


# new_async_session = async_sessionmaker(
#     async_engine, expire_on_commit=False, class_=AsyncSession
# )
# async def get_session():
#     async with new_async_session() as session:
#         yield session