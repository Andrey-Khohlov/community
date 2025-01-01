import asyncio
from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import select, create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uvicorn

from config import settings

app = FastAPI()

engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=False)

new_async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


class CoffeeChatsModel(Base):
    __tablename__: str = "CoffeeChats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    origin: Mapped[str]
    roast_level: Mapped[str]
    flavor_profile: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[str]
''' 
-- Таблица сортов кофе, которые одновременно являются темами обсуждений
CREATE TABLE CoffeeChats (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE, -- Название сорта кофе
    origin VARCHAR(100),              -- Страна происхождения
    roast_level VARCHAR(50),          -- Уровень обжарки: светлая, средняя, темная
    flavor_profile TEXT,              -- Профиль вкуса: "фруктовый, ореховый"
    description TEXT,                 -- Дополнительное описание сорта
    created_at TIMESTAMP DEFAULT NOW()
);
'''

@app.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"Ok": True}


if __name__ == "__main__":
    # uvicorn.run('main:app', host="0.0.0.0", port=80, reload=True)
    uvicorn.run('main:app',  reload=True)