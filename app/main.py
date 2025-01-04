import asyncio
from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import select, create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uvicorn

from app.db.sessions import engine, SessionDep
from app.schemas.coffees import CoffeesAddSchema
from app.db.models.coffees import CoffeesAddModel, Base
from config import settings


app = FastAPI()

@app.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {"Ok": True}

@app.post("/coffee")
async def add_coffee(coffee: CoffeesAddSchema, session: SessionDep):
    new_coffee = CoffeesAddModel(
        **coffee.model_dump(),
    )
    session.add(new_coffee)
    await session.commit()

    return {"Ok": True}

@app.get("/coffee")
async def get_coffee(session: SessionDep):
    query = select(CoffeesAddModel)
    coffee = await session.execute(query)
    return {"Ok": coffee.scalars().all()}

if __name__ == "__main__":
    # uvicorn.run('main:app', host="0.0.0.0", port=80, reload=True)
    uvicorn.run('main:app',  reload=True)