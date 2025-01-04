from pydantic import BaseModel


class CoffeesAddSchema(BaseModel):
    roaster: str
    roasting_level: str
    title: str
    description: str
    price: int
    weight: int
    q_grade_rating: float
    origin: str
    region: str
    farm: str
    farmer: str
    variety: str
    processing: str
    height_min: int
    height_max: int
    yield_: int
    rating: float
    reviews: int
    comments: int
    pack_img: str
    created_at: str

class CoffeesSchema(CoffeesAddSchema):
    id: int