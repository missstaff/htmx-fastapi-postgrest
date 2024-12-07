from secrets import token_hex
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from passlib.hash import pbkdf2_sha256
from models.user.user_hashed import UserCreateHashed, UserLoginHashed
from models.user.user_create import UserCreate
from models.user.user_login import UserLogin
import bcrypt

from controllers.user_controller import authenticate_user, create_user


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/user/create")
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
        response = JSONResponse({"response": response["user_data"]})
        response.headers["hx-redirect"] = "/dashboard"
        return response


@router.post("/user/login")
async def user_login(user: UserLogin) -> HTMLResponse: 
    response = await authenticate_user(user)
    if response["status"] == 200: 
        response = JSONResponse({"response": response["user_data"]})
        response.headers["hx-redirect"] = "/dashboard"
        return response
    else:
        raise HTTPException(status_code=response["status"], detail=response["message"])
