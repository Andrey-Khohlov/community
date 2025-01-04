from pydantic import BaseModel


class UsersAddSchema(BaseModel):
    username: str
    email: str
    password: str
    created_at: str


class UsersSchema(UsersAddSchema):
    id: int