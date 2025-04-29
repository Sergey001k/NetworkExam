from pydantic import BaseModel
from datetime import timedelta


class AdminLoginSchema(BaseModel):
    name: str
    email: str
    password: str


class QuestionCounts(BaseModel):
    network_address: int
    broadcast_address: int
    first_last_address: int


class CreateSessionSchema(BaseModel):
    duration: timedelta
    test_duration: timedelta
    questions: QuestionCounts



