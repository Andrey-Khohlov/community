from datetime import datetime

from pydantic import BaseModel


class UsersAddSchema(BaseModel):
    username: str
    email: str | None = None
    password: str | None = None
    provider: str | None = None
    provider_id: str | None = None
    avatar_url: str | None = None
    is_verified: bool = False
    locality: str | None = None
    language: str | None = None

    is_active: bool = True
    roles: str | None = None


class UsersSchema(UsersAddSchema):
    id: int
    created_at: datetime  # str
    updated_at: datetime  # str

    class Config:
        from_attributes = True  # Работает как старый orm_mode = True