from typing import Dict

from pydantic import BaseModel

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class CoffeesAddSchema(BaseModel):
    origin: str  # Страна
    region: str  # Регион
    locality: str  # Населенный пункт
    farm: str  # Ферма
    farmer: str  # Фермер
    cooperatives: str  # Кооператив
    mill: str  # Станция обработки
    coordinates: Coordinates | None = None  # [6.2000,  38.1500] (["latitude", "longitude"])
    exporter: str  # Экспортер
    importer: str  # Импортер


    variety: str  # Разновидность
    processing: str  # Обработка
    height_min: int  # Высота произрастания мин
    height_max: int  # Высота произрастания макс
    yield_: int  # Дата сбора урожая

    roaster: str  # Обжарщик
    price: int  # Цена
    weight: int  # Вес
    roasting_level: str  # Обжарка
    title: str  # Название
    description: str  # Описание вкуса/аромата

    q_grade_rating: float  # Q-оценка или Оценка SCA

    rating: float  # Рейтинг
    reviews: int  # Оценок
    comments: int  # Комментариев
    tags: str  # Теги
    notes: str  # Примечания

    pack_img: str
    created_by: int


class CoffeesSchema(CoffeesAddSchema):
    id: int
    created_at: str
    updated_at: str

class CoffeeUpdateSchema(BaseModel):
    origin: str | None = None
    region: str | None = None
    locality: str | None = None
    farm: str | None = None
    farmer: str | None = None
    cooperatives: str | None = None
    mill: str | None = None
    coordinates: Coordinates | None = None
    exporter: str | None = None
    importer: str | None = None
    variety: str | None = None
    processing: str | None = None
    height_min: int | None = None
    height_max: int | None = None
    yield_: int | None = None
    roaster: str | None = None
    price: int | None = None
    weight: int | None = None
    roasting_level: str | None = None
    title: str | None = None
    description: str | None = None
    q_grade_rating: float | None = None
    rating: float | None = None
    reviews: int | None = None
    comments: int | None = None
    tags: str | None = None
    notes: str | None = None
    pack_img: str | None = None
    # created_by: int | None = None
