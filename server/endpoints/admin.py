import os

import argon2.exceptions
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from argon2 import PasswordHasher
import datetime

from schemas.admin import AdminRegisterSchema, AdminLoginSchema, CreateSessionSchema, ChangePasswordSchema
from db.db_models import Admin, Session, Result
from utils.jwt import create_access_token, get_current_user, admin_creation_allowed
from utils.exp_check import check_session_expire
from utils.excel_export import export_results

router = APIRouter()
ph = PasswordHasher()


@router.post("/register", status_code=201)
async def register_admin(
        cred: AdminRegisterSchema,
        current_user: dict = Depends(admin_creation_allowed)):

    if len(cred.password) < 8:
        raise HTTPException(status_code=400, detail="Password is too short")

    await Admin.create(name=cred.name, email=cred.email, password=ph.hash(cred.password))

    return {
        "status": "success"
    }


@router.post("/login")
async def login(cred: AdminLoginSchema):
    admin = await Admin.get_or_none(name=cred.name, email=cred.email)
    if admin:
        try:
            ph.verify(admin.password, cred.password)
        except argon2.exceptions.VerificationError:
            raise HTTPException(status_code=401, detail="Invalid user or password")

        token = create_access_token({"id": admin.id,
                                     "role": "admin"}, secret_key=os.getenv("SECRET_KEY"))

        return {
            "access-token": token,
            "token-type": "bearer"
        }

    else:
        raise HTTPException(status_code=401, detail="Invalid user or password")


@router.patch("/change-password", status_code=202)
async def change_password(body: ChangePasswordSchema, current_user: dict = Depends(get_current_user)):
    admin = await Admin.get_or_none(email=body.email, name=body.name)

    if not admin:
        raise HTTPException(status_code=404, detail="Invalid user or password")

    if not ph.verify(admin.password, body.old_password):
        raise HTTPException(status_code=404, detail="Invalid user or password")

    if len(body.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password is too short")

    admin.password = ph.hash(body.new_password)
    await admin.save()

    return {
        "status": "Updated"
    }


@router.post("/create-session", status_code=201)
async def create_session(
        session_parameters: CreateSessionSchema,
        background_tasks: BackgroundTasks,
        current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    session = await Session.create(
        date_started=datetime.datetime.now(),
        duration=session_parameters.test_duration,
        test_duration=session_parameters.test_duration,
        questions_types=session_parameters.questions,
        max_score=10,
        finished=False
    )

    background_tasks.add_task(check_session_expire, session.id, session.date_started+session.duration)


@router.get("/get-sessions")
async def get_all_session(
        current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    sessions = await Session.all()
    return sessions


@router.get("/get-results/{session_id}")
async def get_session_results(
        session_id,
        current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    if not (await Session.get_or_none(id=session_id)):
        raise HTTPException(status_code=404, detail="Session not found")

    results = await Result.filter(session_id=session_id)
    return results


@router.get("/export-results/{session_id}")
async def export_results_xls(
        session_id,
        current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    session = await Session.get_or_none(id=session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    results = await Result.filter(session=session)

    buffer, filename = await export_results(list(results), session_date=session.date_started)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename="+filename}
    )
