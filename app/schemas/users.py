from pydantic import BaseModel


class UsersAddSchema(BaseModel):
    username: str
    email: str
    password: str
    provider: str
    provider_id: str
    avatar_url: str
    is_verified: bool
    locality: str
    language: str

    is_active: bool
    roles: str
    last_login: str


class UsersSchema(UsersAddSchema):
    id: int
    created_at: str
    updated_at: str
