import datetime
from typing import Annotated, Optional

from sqlalchemy import func, text
from sqlalchemy.orm import  Mapped, mapped_column

from app.db.models import Model, intpk, created_at, updated_at


class CommentsAddModel(Model):
    __tablename__: str = "comments"
    id: Mapped[intpk]
    product_id: Mapped[int]
    user_id: Mapped[int]
    content: Mapped[str]
    parent_id: Mapped[Optional[int]]
    review_id: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]