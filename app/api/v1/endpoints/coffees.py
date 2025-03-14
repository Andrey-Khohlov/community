from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db.models.coffees import CoffeesAddModel
from app.db.sessions import SessionDep
from app.schemas.coffees import CoffeesAddSchema, CoffeeUpdateSchema

router = APIRouter()

@router.post("/")
async def add_coffee(coffee: CoffeesAddSchema, session: SessionDep):
    new_coffee = CoffeesAddModel(**coffee.model_dump())
    session.add(new_coffee)
    await session.commit()
    return {"Ok": True}

@router.get("/")
async def get_coffee(session: SessionDep):
    query = select(CoffeesAddModel)
    coffee = await session.execute(query)
    return {"Ok": coffee.scalars().all()}


# Endpoint для обновления карточки кофе
@router.put("/{coffee_id}")
async def update_coffee(coffee_id: int, coffee_update: CoffeeUpdateSchema, session: SessionDep):
    # Создаем запрос с условием where
    query = select(CoffeesAddModel).where(CoffeesAddModel.id == coffee_id)

    # Выполняем запрос
    result = await session.execute(query)

    # Получаем первую запись (если она есть)
    coffee = result.scalars().first()

    # Если кофе с таким id не найден, возвращаем 404
    if coffee is None:
        raise HTTPException(status_code=404, detail="Coffee not found")

    # Обновляем поля, если они переданы
    for field, value in coffee_update.model_dump(exclude_unset=True).items():
        setattr(coffee, field, value)

    # Сохраняем изменения в базе данных
    await session.commit()
    await session.refresh(coffee)

    # Возвращаем обновленный объект
    return {"Ok": coffee}