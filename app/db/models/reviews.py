from typing import Optional

from sqlalchemy.orm import  Mapped, mapped_column

from app.db.models import Model, str_256, intpk, created_at, updated_at


class ReviewsAddModel(Model):
    __tablename__: str = "reviews"
    id: Mapped[intpk]
    user_id: Mapped[int]
    coffee_id: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    rating_2: Mapped[int]=mapped_column(default=0)
    rating_4: Mapped[Optional[int]]
    rating_20: Mapped[Optional[int]]
    tags: Mapped[Optional[str]]
    pack_img: Mapped[Optional[str]]
    method: Mapped[str]
    receipt: Mapped[Optional[str]]
    water: Mapped[str]
    water_ppm: Mapped[Optional[int]]
    water_pH: Mapped[Optional[float]]
    water_receipt: Mapped[Optional[str]]
    temperature: Mapped[Optional[int]]
    grinder: Mapped[Optional[str]]
    grinding: Mapped[Optional[str]]
    filter: Mapped[Optional[str]]
    cafe: Mapped[Optional[str]]