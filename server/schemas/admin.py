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
    same_network: int
    mask_count: int
    mask_range: int
    host_addr: int


class CreateSessionSchema(BaseModel):
    duration: timedelta
    test_duration: timedelta
    questions: QuestionCounts


class ChangePasswordSchema(BaseModel):
    name: str
    email: EmailStr
    old_password: str
    new_password: str

