from sqlalchemy.orm import  Mapped, mapped_column

from app.db.models import Model, str_256, intpk, created_at, updated_at


class UsersAddModel(Model):
    __tablename__: str = "users"
    id: Mapped[intpk]
    username: Mapped[str_256]
    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]