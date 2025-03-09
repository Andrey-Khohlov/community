'''5.
reviews Отзывы о кофе (coffee_reviews)
-------
id (PK)              - Уникальный идентификатор отзыва
user_id (FK)         - ID пользователя, оставившего отзыв
coffee_id (FK)       - ID сорта кофе
text                 - Текст отзыва
tags
rating_2             - Оценка 0 или 1
rating_4             - Оценка от 1 до 5
rating_20            - Оценка от 80 до 100
created_at           - Дата отзыва
pack_img             - Фото пачки
method               - V60, джезва, эспрессо, мокка...
    Эспрессо
    Пуровер
    Капельная кофеварка
    Джезва
    Френч-пресс
    Гейзерная кофеварка
    Иммерсионная воронка
    В чашке
    Аэропресс
    Капсулы
    Дрип-пакеты
    Брю-бэги

receipt              - рецепт приготовления
water
water_ppm
water_pH
water_receipt
temperature
grinder
grinding
filter ?
cafe                 - last 5: кафе'''
from typing import Optional

from pydantic import BaseModel, confloat


class ReviewsAddSchema(BaseModel):
    user_id: int
    coffee_id: int

    rating: Optional[confloat(ge=1, le=5.9)]

    method: str

    grinder: str
    grinding: float
    filter: str
    water: str
    temperature: int
    brew_time: str
    receipt: str

    cafe: str

    experience: str
    tags: str

    pack_img: str

class ReviewsSchema(ReviewsAddSchema):
    id: int
    created_at: str
    updated_at: str