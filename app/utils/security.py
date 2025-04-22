import jwt
from jwt import PyJWTError
import bcrypt
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
import os

SECRET_KEY = os.getenv('SECRET_KEY', '')
ALGORITHM = os.getenv('ALGORITHM', '')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('TOKEN_EXPIRE_MIN', '30'))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    to_encode.update({"role": data.get("role")})
    to_encode.update({"sub": data.get("sub")})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
        return user_id, role
    except PyJWTError:
        raise credentials_exception
