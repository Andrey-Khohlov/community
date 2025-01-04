from fastapi import APIRouter
from sqlalchemy import select

from app.db.models.coffees import CoffeesAddModel
from app.db.sessions import SessionDep
from app.schemas.coffees import CoffeesAddSchema


router = APIRouter()

@router.post("/coffees")
async def add_coffee(coffee: CoffeesAddSchema, session: SessionDep):
    new_coffee = CoffeesAddModel(**coffee.model_dump())
    session.add(new_coffee)
    await session.commit()
    return {"Ok": True}

@router.get("/coffees")
async def get_coffee(session: SessionDep):
    query = select(CoffeesAddModel)
    coffee = await session.execute(query)
    return {"Ok": coffee.scalars().all()}

