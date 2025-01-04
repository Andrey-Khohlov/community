from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class CoffeesAddModel(Base):
    __tablename__: str = "coffees"
    id: Mapped[int] = mapped_column(primary_key=True)
    roaster: Mapped[str]
    roasting_level: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    weight: Mapped[int]
    q_grade_rating: Mapped[float]
    origin: Mapped[str]
    region: Mapped[str]
    farm: Mapped[str]
    farmer: Mapped[str]
    variety: Mapped[str]
    processing: Mapped[str]
    height_min: Mapped[int]
    height_max: Mapped[int]
    yield_: Mapped[int]
    rating: Mapped[float]
    reviews: Mapped[int]
    comments: Mapped[int]
    pack_img: Mapped[str]
    created_at: Mapped[str]

class CoffeeChatsModel(Base):
    """ Создание таблицы
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
    """
    __tablename__: str = "coffee_сhats"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    origin: Mapped[str]
    roast_level: Mapped[str]
    flavor_profile: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[str]