from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String, Boolean

from app.db.models import Model, str_256, intpk, created_at, updated_at

# Ленивый импорт для CommentsAddModel
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.db.models.comments import CommentsAddModel


# class UsersAddModel(Model):
#     __tablename__: str = "users"
#     id: Mapped[intpk]
#     username: Mapped[str_256]
#     email: Mapped[str]
#     password: Mapped[str]
#     created_at: Mapped[created_at]
#     updated_at: Mapped[updated_at]
#     comment: Mapped[list["CommentsAddModel"]] = relationship( "CommentsAddModel", back_populates="user", lazy="dynamic", cascade="all, delete, delete-orphan" )


class UsersAddModel(Model):
    __tablename__: str = "users"

    id: Mapped[intpk]
    username: Mapped[str_256]
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)  # ← nullable для OAuth
    password: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # ← nullable для OAuth

    # Новые поля для OAuth
    provider: Mapped[Optional[str_256]] = mapped_column(String(256), nullable=True)  # google, facebook и т.д.
    provider_id: Mapped[Optional[str_256]] = mapped_column(String(256), nullable=True, unique=True)  # ID из соцсети
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # аватар из соцсети
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)  # подтвержден ли email
    locality: Mapped[Optional[str_256]] = mapped_column(String(256), nullable=True)  # населённый пункт
    language: Mapped[Optional[str_256]] = mapped_column(String(256), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    roles: Mapped[Optional[str_256]] = mapped_column(String(256), nullable=True)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    comment: Mapped[list["CommentsAddModel"]] = relationship(
        "CommentsAddModel",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete, delete-orphan"
    )

    __table_args__ = (
        Index('idx_provider_provider_id', 'provider', 'provider_id', unique=True),
    )