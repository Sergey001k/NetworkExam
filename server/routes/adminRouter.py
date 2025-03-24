import jwt
import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException
from schemas.admin import AdminLoginSchema, CreateTestShema
from db.db_models import Admin
from utils.jwt import create_acces_token
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/login")
async def login(cred: AdminLoginSchema):
    admin = await Admin.get_or_none(name=cred.name, surname=cred.surname, email=cred.email)
    if admin:
        if cred.password == admin.password:
            
            token = create_acces_token({"id": admin.id})
            
            return {
                "acces-token": token,
                "token-type": "bearer"
            }
        
        else:
            raise HTTPException(status_code=401, detail="Invalid Password")

    raise HTTPException(status_code=401, detail="Invalid Data")


@router.post("/create")
def create_test(test: CreateTestShema):
    ...
