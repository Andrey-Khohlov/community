from pydantic import BaseModel


class CoffeesAddSchema(BaseModel):
    roaster: str  # Обжарщик
    roasting_level: str  # Обжарка
    title: str  # Название
    description: str  # Описание
    price: int  # Цена
    weight: int  # Вес
    q_grade_rating: float  # Q-оценка
    origin: str  # Страна
    region: str  # Регион
    farm: str  # Ферма/Станция
    farmer: str  # Производитель
    variety: str  # Разновидность
    processing: str  # Обработка
    height_min: int  # Высота произрастания
    height_max: int  # Высота произрастания
    yield_: int  # Урожай
    rating: float  # Рейтинг
    reviews: int  # Оценок
    comments: int  # Комментариев
    pack_img: str


class CoffeesSchema(CoffeesAddSchema):
    id: int
    created_at: str