import os
import bcrypt
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from models.user.user_hashed import UserCreateHashed
from models.user.user_create import UserCreate
from models.user.user_login import UserLogin
from controllers.user_controller import authenticate_user, create_user


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

load_dotenv(f".env.{os.getenv('APP_ENV', 'local')}")
EXPIRATION_TIME = os.getenv("EXPIRATION_TIME")

@router.post("/user/create", response_class=HTMLResponse)
async def user_create(user: UserCreate)-> HTMLResponse:   
    bytes = user.password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    hash_password = bcrypt.hashpw(bytes, salt) 
    
    hashed_user = UserCreateHashed(
    name=user.name, 
    display_name=user.display_name,
    email=user.email,
    salt=salt, 
    hash_password=hash_password)

    response = await create_user(hashed_user)
    if response["status"] == 201:
        response_json = JSONResponse({"response": response["user_data"]})
        response_json.headers["Authorization"] = f"Bearer {response['access_token']}"
        response_json.headers["hx-redirect"] = "/dashboard"
        response_json.set_cookie(
            key="access_token", 
            value=response['access_token'],
            max_age=EXPIRATION_TIME,
            #httponly=True,  # Helps mitigate XSS attacks
            #secure=True,  # Use only for HTTPS
            # samesite="Strict" 
        )
        return response_json
    else:
        raise HTTPException(status_code=response["status"], detail=response["message"])


@router.post("/user/login", response_class=HTMLResponse)
async def user_login(user: UserLogin) -> HTMLResponse: 
    response = await authenticate_user(user)
    if response["status"] == 200: 
        response_json = JSONResponse({"response": response["user_data"]})
        response_json.headers["Authorization"] = f"Bearer {response['access_token']}"
        response_json.headers["hx-redirect"] = "/dashboard"
        response_json.set_cookie(
            key="access_token", 
            value=response['access_token'],
            max_age=EXPIRATION_TIME,
            #httponly=True,  # Helps mitigate XSS attacks
            #secure=True,  # Use only for HTTPS
            # samesite="Strict" 
        )
        return response_json
    else:
        raise HTTPException(status_code=response["status"], detail=response["message"])
