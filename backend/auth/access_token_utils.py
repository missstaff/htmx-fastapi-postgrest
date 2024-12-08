import os
from dotenv import load_dotenv
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

environment = os.getenv("APP_ENV", "local")
dotenv_file = f".env.{environment}" 
load_dotenv(dotenv_file)
JWT_KEY = os.getenv("JWT_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        return payload 
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
