from pydantic import BaseModel


class StudentRegisterSchema(BaseModel):
    name: str
    group: str
    session_id: int
