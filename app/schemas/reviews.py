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

from pydantic import BaseModel


class ReviewsAddSchema(BaseModel):
    user_id: int
    coffee_id: int
    tags: str
    rating_2: int
    rating_4: int | None
    rating_20: int | None
    pack_img: str
    method: str
    receipt: str
    water: str
    water_ppm: int
    water_pH: float
    water_receipt: str
    temperature: int
    grinder: str
    grinding: str
    filter: str
    cafe: str


class ReviewsSchema(ReviewsAddSchema):
    id: int
    created_at: str
    updated_at: str