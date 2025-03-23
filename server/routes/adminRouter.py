from fastapi import APIRouter
from schemas.admin import AdminLoginSchema

router = APIRouter()

@router.post("/login")
def login(cred: AdminLoginSchema):
    return "Succes"