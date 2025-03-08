from sqlalchemy.orm import  Mapped, mapped_column

from app.db.models import Model, intpk, created_at, updated_at, RoastingLevel, str_256


class CoffeesAddModel(Model):
    __tablename__: str = "coffees"
    id: Mapped[intpk]
    created_at: Mapped[created_at]
    # 1 строка
    title: Mapped[str_256]
    yield_: Mapped[int]
    processing: Mapped[str_256]
    variety: Mapped[str_256]
    height_min: Mapped[int]
    height_max: Mapped[int]
    # 2 строка
    origin: Mapped[str_256]
    region: Mapped[str_256]
    farm: Mapped[str_256]
    farmer: Mapped[str_256]
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
    created_by: Mapped[int]
    notes: Mapped[str]
    updated_at: Mapped[updated_at]
    exporter: Mapped[str_256]
    importer: Mapped[str_256]
    subregion: Mapped[str_256]
    plant: Mapped[str_256]

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