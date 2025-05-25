import os
import json
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from utils.questions_generator import QuestionGenerator
from utils.jwt import create_access_token, get_active_student
from db.db_models import Student, Question, Session, Result
from schemas.student import StudentRegisterSchema, SafeQuestionOut, SendAnswerSchema

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
            session=session)

    token = create_access_token(data={
        "id": student.id,
        "session_id": session.id,
        "role": "student"
    }, secret_key=os.getenv("SECRET_KEY"))

    return {
        "access-token": token,
        "token-type": "bearer"
    }


@router.get("/get-questions", response_model=List[SafeQuestionOut])
async def get_questions(
        current_user: dict = Depends(get_active_student)):
    questions = await Question.filter(student_id=current_user["id"])

    if questions:
        return await Question.filter(student_id=current_user["id"])

    session = await Session.get(id=current_user["session_id"])
    student = await Student.get(id=current_user["id"])

    if not session:
        raise HTTPException(404, detail="Session not found")

    questions = QuestionGenerator.generate_questions(session.questions_types)

    for question in questions:
        q_type = question["type"]
        question.pop("type", None)
        await Question.create(
            session=session,
            student=student,
            type=q_type,
            question=json.dumps(question)
        )

    return await Question.filter(student_id=current_user["id"])


@router.patch("/send-answer", status_code=202)
async def send_answer(
        body: List[SendAnswerSchema],
        current_user: dict = Depends(get_active_student)):

    student = await Student.get(id=current_user["id"])
    session = await Session.get_or_none(id=current_user['session_id'])

    if await Result.get_or_none(session=session, student_name=student.name):
        raise HTTPException(403, detail="Results have already been sent")

    score = 0

    for st_answer in body:
        question = await Question.get(id=st_answer.question_id, student=student)
        question.question["student_answer"] = st_answer.answer

        if question.question["corr_answer"] == st_answer.answer:
            score += 1

        await question.save()

    percent = score/session.max_score * 100

    await Result.create(
        session=session,
        student_name=student.name,
        group=student.group,
        score=score,
        percent=percent
    )

    return {
        "score": score,
        "percent": percent
    }
