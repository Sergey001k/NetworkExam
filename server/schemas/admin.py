from pydantic import BaseModel, EmailStr
from datetime import timedelta


class AdminRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class AdminLoginSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class QuestionCounts(BaseModel):
    network_address: int
    broadcast_address: int
    first_last_address: int


class CreateSessionSchema(BaseModel):
    duration: timedelta
    test_duration: timedelta
    questions: QuestionCounts



