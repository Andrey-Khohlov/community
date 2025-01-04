from sqlalchemy.orm import  Mapped, mapped_column

from app.db.models import Model


class UsersAddModel(Model):
    __tablename__: str = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[str]