from enum import Enum as PyEnum
from sqlalchemy import Enum

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import  Mapped, mapped_column

from app.db.models import Model, intpk, created_at, updated_at, RoastingLevel, str_256, CoffeeProcessing, Origin


class CoffeesAddModel(Model):
    __tablename__: str = "coffees"
    id: Mapped[intpk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    # 1 строка место
    origin: Mapped[Origin] = mapped_column(Enum(Origin, name="origin_enum"))
    region: Mapped[str_256]
    locality: Mapped[str_256]
    farm: Mapped[str_256]
    farmer: Mapped[str_256]
    cooperatives: Mapped[str_256]
    mill: Mapped[str_256]
    coordinates: Mapped[dict | None] = mapped_column(JSONB, nullable=True)   # указывает на ферму или милл или кооператив или локалити
    exporter: Mapped[str_256]
    importer: Mapped[str_256]
    # 2 строка зерно
    variety: Mapped[str_256]
    processing: Mapped[CoffeeProcessing] = mapped_column(Enum(CoffeeProcessing, name="processing_enum"))
    height_min: Mapped[int]
    height_max: Mapped[int]
    yield_: Mapped[int]
    # 3 строка обжар
    roaster: Mapped[str]
    price: Mapped[int]
    weight: Mapped[int]
    roasting_level: Mapped[RoastingLevel]
    title: Mapped[str_256]  # без указания страны в названии
    description: Mapped[str]
    # 4 строка оценки
    q_grade_rating: Mapped[float]
    rating: Mapped[float]
    reviews: Mapped[int]
    comments: Mapped[int]
    tags: Mapped[str]
    notes: Mapped[str]

    # не выводится
    pack_img: Mapped[str]
    created_by: Mapped[int]


# class CoffeeChatsModel(Model):
#     """ Создание таблицы
#     -- Таблица сортов кофе, которые одновременно являются темами обсуждений
#     CREATE TABLE CoffeeChats (
#         id SERIAL PRIMARY KEY,
#         name VARCHAR(100) NOT NULL UNIQUE, -- Название сорта кофе
#         origin VARCHAR(100),              -- Страна происхождения
#         roast_level VARCHAR(50),          -- Уровень обжарки: светлая, средняя, темная
#         flavor_profile TEXT,              -- Профиль вкуса: "фруктовый, ореховый"
#         description TEXT,                 -- Дополнительное описание сорта
#         created_at TIMESTAMP DEFAULT NOW()
#     );
#     """
#     __tablename__: str = "coffee_сhats"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#     origin: Mapped[str]
#     roast_level: Mapped[str]
#     flavor_profile: Mapped[str]
#     description: Mapped[str]
#     created_at: Mapped[str]