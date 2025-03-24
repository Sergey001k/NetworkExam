import jwt
import os
from datetime import datetime, timedelta, timezone

def create_acces_token(data: dict):
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": exp})
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALG = os.getenv("ALGORITHM")

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALG)

