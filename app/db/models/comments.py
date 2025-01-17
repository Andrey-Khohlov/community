from typing import Annotated, Optional

from sqlalchemy import func, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import Model, intpk, created_at, updated_at


class CommentsAddModel(Model):
    __tablename__: str = "comments"
    id: Mapped[intpk]
    product_id: Mapped[int]
    user_id: Mapped[int] #= mapped_column(ForeignKey("UsersAddModel.id"))
    content: Mapped[str]
    parent_id: Mapped[Optional[int]]
    review_id: Mapped[int]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    # user: Mapped["UsersAddModel"] = relationship("UsersAddModel", back_populates="comment")
