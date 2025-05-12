from pydantic import BaseModel


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


class SendAnswerSchema(BaseModel):
    question_id: int
    answer: str | dict
