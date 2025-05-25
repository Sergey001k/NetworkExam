from pydantic import BaseModel
from typing import List, Dict


class StudentRegisterSchema(BaseModel):
    name: str
    group: str
    session_id: int


class TestGenerationSchema(BaseModel):
    network_address: int
    broadcast_address: int
    first_last_address: int
    same_network: int
    mask_count: int
    mask_range: int
    host_addr: int


class SafeQuestionBodyOut(BaseModel):
    question: str | List | Dict
    student_answer: str | None


class SafeQuestionOut(BaseModel):
    session_id: int
    id: int
    type: str
    student_id: int
    question: SafeQuestionBodyOut

    class Config:
        from_attributes = True


class SendAnswerSchema(BaseModel):
    question_id: int
    answer: str | dict
