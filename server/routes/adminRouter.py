import argon2.exceptions
from fastapi import APIRouter, HTTPException, Depends
from argon2 import PasswordHasher
import datetime

from schemas.admin import AdminLoginSchema, CreateSessionSchema
from db.db_models import Admin, Session, Result
from utils.jwt import create_access_token, get_current_user, security


router = APIRouter()
ph = PasswordHasher()


@router.post("/login")
async def login(cred: AdminLoginSchema):
    admin = await Admin.get_or_none(name=cred.name, surname=cred.surname, email=cred.email)
    if admin:
        try:
            ph.verify(admin.password, cred.password)
        except argon2.exceptions.VerificationError:
            raise HTTPException(status_code=401, detail="Invalid user or password")

        token = create_access_token({"id": admin.id})

        return {
            "access-token": token,
            "token-type": "bearer"
        }

    else:
        raise HTTPException(status_code=401, detail="Invalid user or password")


@router.post("/create-session", status_code=201)
async def create_session(session_parameters: CreateSessionSchema, current_user: dict = Depends((get_current_user))):
    await Session.create(
        date_started=datetime.datetime.now(),
        duration=session_parameters.test_duration,
        test_duration=session_parameters.test_duration,
        questions=session_parameters.questions,
        max_score=10,
        finished=False
    )


@router.get("/get-sessions")
async def get_all_session(current_user: dict = Depends((get_current_user))):
    sessions = await Session.all()
    return sessions


@router.get("/get-results/{session_id}")
async def get_session_results(session_id, current_user: dict = Depends(get_current_user)):
    if not(Session.get_or_none(id=session_id)):
        raise HTTPException(status_code=404, detail="Session not found")

    results = await Result.filter(session_id=session_id)

    return results
