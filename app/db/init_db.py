import time

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.models import Model, RoastingLevel
from app.db.models.coffees import CoffeesAddModel
from app.db.models.comments import CommentsAddModel
from app.db.models.reviews import ReviewsAddModel
from app.db.models.users import UsersAddModel
from app.db.sessions import engine, SessionDep, get_session, new_async_session

coffe_dict = [
    {
    "roaster": "Tasty",
    "roasting_level": RoastingLevel.filter,
    "title": "Ла Кабана",
    "description": "Яркий кофе с нотами грейпфрута, вишни, красного вермута и тёмного шоколада",
    "price": 1029,
    "weight": 250,
    "q_grade_rating": 86.5,
    "origin": "Гватемала",
    "region": "Санта Роза",
    "farm": "Ла Кабана",
    "farmer": "Исауро Балерио Соларес",
    "variety": "бурбон",
    "processing": "натуральный анаэробный",
    "height_min": 1600,
    "height_max": 1600,
    "yield_": 2024,
    "rating": 4.5,
    "reviews": 1,
    "comments": 1,
    "pack_img": "..."
},
    {
    "roaster": "Tasty",
    "roasting_level": RoastingLevel.filter,
    "title": "Берату Шакиту",
    "description": "Сладкий кофе с нотами красного апельсина, чёрной смородины, и чёрного чая",
    "price": 919,
    "weight": 250,
    "q_grade_rating": 86.5,
    "origin": "Эфиопия",
    "region": "Гедеб",
    "farm": "Челчеле",
    "farmer": "",
    "variety": "местные",
    "processing": "натуральный анаэробный",
    "height_min": 1600,
    "height_max": 1600,
    "yield_": 2024,
    "rating": 4.5,
    "reviews": 1,
    "comments": 1,
    "pack_img": "..."
    }
]

reviews_dict = [
    {
    "user_id": 1,
    "coffee_id": 1,
    "tags": "фруктовый",
    "rating_2": 1,
    "rating_4": 4,
    "rating_20": None,
    "pack_img": "...",
    "method": "V60",
    "receipt": None,
    "water": "Шишкин лес",
    "water_ppm": 60,
    "water_pH": 7.0,
    "water_receipt": None,
    "temperature": 95,
    "grinder": "Sculptor070",
    "grinding": "6",
    "filter": "T-90",
    "cafe": None,
    },
    {
    "user_id": 1,
    "coffee_id": 2,
    "tags": "фруктовый",
    "rating_2": 1,
    "rating_4": 5,
    "rating_20": None,
    "pack_img": "...",
    "method": "V60",
    "receipt": "5 минут проливал",
    "water": "Пилигрим",
    "water_ppm": 60,
    "water_pH": 7.0,
    "water_receipt": None,
    "temperature": 92,
    "grinder": "Sculptor070",
    "grinding": "6",
    "filter": "T-90",
    "cafe": None,
    }
]

comments_dict = [
    {
    "product_id": 1,
    "user_id": 1,
    "content": "Вкусный кофеёк",
    "parent_id": None,
    "review_id": 1,
    },
    {
    "product_id": 1,
    "user_id": 2,
    "content": "Кофе отличный, легкий, ягодный.",
    "parent_id": 1,
    "review_id": 1,
    },
    {
    "product_id": 1,
    "user_id": 1,
    "content": "Неплохой вариант оказался, вкусно! Варим кофе в кофе машине Philips, так как некогда заморочиться с приготовлением кофе другими способами!",
    "parent_id": 2,
    "review_id": 1,
    },
]

async def setup_database():
    engine.echo = False
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
        await conn.run_sync(Model.metadata.create_all)
    engine.echo = True
    return {"DB has been created": True}


async def insert_init_data():

    async with new_async_session() as session:
        user1 = UsersAddModel(username="admin", email="admin", password="admin")
        user2 = UsersAddModel(username="user", email="user", password="user")
        coffees = [CoffeesAddModel(**coffee) for coffee in coffe_dict]
        reviews = [ReviewsAddModel(**review) for review in reviews_dict]
        comments = [CommentsAddModel(**comment) for comment in comments_dict]
        session.add_all([user1, user2])
        session.add_all(coffees)
        session.add_all(reviews)
        session.add_all(comments)
        await session.commit()
    return {"Data has been inserted": True}
