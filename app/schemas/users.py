from pydantic import BaseModel


class UsersAddSchema(BaseModel):
    username: str
    email: str
    password: str


class UsersSchema(UsersAddSchema):
    id: int
    created_at: str
    updated_at: str