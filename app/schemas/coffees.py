from pydantic import BaseModel


class CoffeesAddSchema(BaseModel):

    title: str  # Название
    yield_: int  # Урожай
    processing: str  # Обработка
    variety: str  # Разновидность
    height_min: int  # Высота произрастания
    height_max: int  # Высота произрастания

    origin: str  # Страна
    region: str  # Регион
    farm: str  # Ферма/Станция
    farmer: str  # Производитель

    roaster: str  # Обжарщик
    price: int  # Цена
    weight: int  # Вес
    q_grade_rating: float  # Q-оценка
    rating: float  # Рейтинг
    reviews: int  # Оценок
    comments: int  # Комментариев
    roasting_level: str  # Обжарка

    description: str  # Описание

    pack_img: str
    created_by: int
    notes: str
    updated_at: str
    exporter: str
    importer: str
    subregion: str
    plant: str


class CoffeesSchema(CoffeesAddSchema):
    id: int
    created_at: str