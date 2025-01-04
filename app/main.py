import asyncio
from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import select, create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uvicorn

from config import settings
from app.db.models.coffee import CoffeesAddModel, Base

app = FastAPI()

engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=False)

new_async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class CoffeesAddSchema(BaseModel):
    roaster: str
    roasting_level: str
    title: str
    description: str
    price: int
    weight: int
    q_grade_rating: float
    origin: str
    region: str
    farm: str
    farmer: str
    variety: str
    processing: str
    height_min: int
    height_max: int
    yield_: int
    rating: float
    reviews: int
    comments: int
    pack_img: str
    created_at: str

class CoffeesSchema(CoffeesAddSchema):
    id: int


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