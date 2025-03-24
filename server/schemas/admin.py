from pydantic import BaseModel

class AdminLoginSchema(BaseModel):
    name: str
    surname: str
    email: str
    password: str

class CreateTestShema(BaseModel):
    questions: str
    duration: str