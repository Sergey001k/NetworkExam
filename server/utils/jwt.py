import jwt
import os
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from fastapi import HTTPException
from db.db_models import Admin, Session


security = HTTPBearer()


def create_access_token(data: dict, secret_key):
    to_encode = data.copy()

    exp_time = int(os.getenv("JWT_EXP"))
    exp = datetime.now(timezone.utc) + timedelta(minutes=exp_time)
    to_encode.update({"exp": exp})

    return jwt.encode(to_encode, secret_key, algorithm="HS256")


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")


async def admin_creation_allowed(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    if not list(await Admin.all()):
        return True

    try:
        token = credentials.credentials
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])

        if payload["role"] != "admin":
            raise HTTPException(status_code=403, detail="Permission denied")

        if not await Admin.get_or_none(id=payload[id]):
            raise HTTPException(status_code=404, detail="Admin not found")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")


async def get_active_student(current_user: dict = Depends(get_current_user)):
    session = await Session.get_or_none(id=current_user["session_id"])
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.finished:
        raise HTTPException(status_code=403, detail="Forbidden")

    return current_user
