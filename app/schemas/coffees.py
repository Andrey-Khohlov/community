from typing import Dict

from pydantic import BaseModel

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class CoffeesAddSchema(BaseModel):

    origin: str  # Страна
    region: str  # Регион
    locality: str
    cooperatives: str
    farm: str  # Ферма/Станция
    farmer: str  # Производитель
    mill: str
    coordinates: Coordinates | None = None  # {"latitude": 6.2000, "longitude": 38.1500}
    exporter: str
    importer: str


    variety: str  # Разновидность
    processing: str  # Обработка
    height_min: int  # Высота произрастания
    height_max: int  # Высота произрастания
    yield_: int  # Урожай

    roaster: str  # Обжарщик
    price: int  # Цена
    weight: int  # Вес
    roasting_level: str  # Обжарка
    title: str  # Название
    description: str  # Описание

    q_grade_rating: float  # Q-оценка
    rating: float  # Рейтинг
    reviews: int  # Оценок
    comments: int  # Комментариев
    tags: str  # Теги
    notes: str  # Примечания

    pack_img: str
    created_by: int
    updated_at: str

class CoffeesSchema(CoffeesAddSchema):
    id: int
    created_at: str