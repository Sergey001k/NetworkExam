from fastapi import APIRouter, HTTPException, Depends
from schemas.admin import AdminLoginSchema, CreateTestShema
from db.db_models import Admin
from utils.jwt import create_acces_token, get_current_user, security
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
async def create_test(test: CreateTestShema, current_user: dict = Depends(get_current_user)):
    return {
        "message": "Test created successfully",
        "user_id": current_user["id"],
    }