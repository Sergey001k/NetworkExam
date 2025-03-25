import jwt
import os
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from fastapi import Depends
from fastapi import HTTPException

security = HTTPBearer()

def create_acces_token(data: dict):
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": exp})
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALG = os.getenv("ALGORITHM")

    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

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
