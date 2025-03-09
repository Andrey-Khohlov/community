from typing import Optional

from pydantic import confloat
from sqlalchemy.orm import  Mapped, mapped_column

from app.db.models import Model, str_256, intpk, created_at, updated_at, BrewMethod


class ReviewsAddModel(Model):
    __tablename__: str = "reviews"
    id: Mapped[intpk]
    user_id: Mapped[int]
    coffee_id: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    rating: Mapped[Optional[float]]

    method: Mapped[BrewMethod]

    grinder: Mapped[Optional[str]]
    grinding: Mapped[Optional[float]]
    filter: Mapped[Optional[str_256]]
    water: Mapped[str]
    temperature: Mapped[Optional[int]]
    brew_time: Mapped[Optional[str_256]]
    receipt: Mapped[Optional[str]]

    cafe: Mapped[Optional[str_256]]

    experience: Mapped[Optional[str]]
    tags: Mapped[Optional[str]]

    pack_img: Mapped[Optional[str]]