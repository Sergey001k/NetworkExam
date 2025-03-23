from pydantic import BaseModel

class AdminLoginSchema(BaseModel):
    username: str
    email: str
    password: str