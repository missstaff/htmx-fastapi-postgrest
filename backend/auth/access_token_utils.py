import os
from dotenv import load_dotenv
import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv(f".env.{os.getenv('APP_ENV', 'local')}")
JWT_KEY = os.getenv("JWT_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        return payload 
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
