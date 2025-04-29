import os

from fastapi import APIRouter, HTTPException, Depends

from utils.questions_generator import QuestionGenerator
from utils.jwt import create_access_token, get_current_user
from db.db_models import Student, Question, Session
from schemas.student import StudentRegisterSchema

router = APIRouter()


@router.post("/register")
async def register_student(cred: StudentRegisterSchema):
    student = await Student.get_or_none(name=cred.name, group=cred.group)
    session = await Session.get_or_none(id=cred.session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.finished:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not student:
        student = await Student.create(
            name=cred.name,
            group=cred.group,
            session_id=session)

    token = create_access_token(data={
        "id": student.id,
        "session_id": session.id,
        "role": "student"
    }, secret_key=os.getenv("SECRET_KEY"))

    return {
        "access-token": token,
        "token-type": "bearer"
    }


@router.get("/get-questions")
async def get_questions(
        current_user: dict = Depends(get_current_user)):
    questions = await Question.filter(student_id=current_user["id"])
    if not questions:
        raise HTTPException(status_code=401, detail="Questions not found")

    return questions

# TODO: Сделать запись вопросов в базу данных
@router.post("/generate-questions")
async def generate_questions():
    pass
