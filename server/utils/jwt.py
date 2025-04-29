import jwt
import os
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from fastapi import HTTPException

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
