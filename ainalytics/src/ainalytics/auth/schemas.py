from pydantic import BaseModel


class UserCheck(BaseModel):
    email: str


class UserCreate(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    id: int
    email: str
    password: str


class GoogleAuth(BaseModel):
    email: str
    token: str
