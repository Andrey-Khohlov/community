from sqlalchemy.orm import  Mapped, mapped_column

from app.db.models import Model, intpk, created_at, updated_at, RoastingLevel


class CoffeesAddModel(Model):
    __tablename__: str = "coffees"
    id: Mapped[intpk]
    created_at: Mapped[created_at]
    # 1 строка
    title: Mapped[str]
    yield_: Mapped[int]
    processing: Mapped[str]
    variety: Mapped[str]
    height_min: Mapped[int]
    height_max: Mapped[int]
    # 2 строка
    origin: Mapped[str]
    region: Mapped[str]
    farm: Mapped[str]
    farmer: Mapped[str]
    # 3 строка
    roaster: Mapped[str]
    price: Mapped[int]
    weight: Mapped[int]
    q_grade_rating: Mapped[float]
    rating: Mapped[float]
    reviews: Mapped[int]
    comments: Mapped[int]
    roasting_level: Mapped[RoastingLevel]
    # 4 строка
    description: Mapped[str]
    # не выводится
    pack_img: Mapped[str]
    updated_at: Mapped[updated_at]
    exporter: Mapped[str]
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