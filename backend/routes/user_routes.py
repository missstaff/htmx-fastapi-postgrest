from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from models.user.user_login import UserLogin
from models.user.user_create import UserCreate
from controllers.user_controller import authenticate_user, create_user


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/user/create")
async def user_create(user: UserCreate):  
   response = await create_user(user)
   if response["status"] == 201:
        response = JSONResponse({"response": response["user_data"]})
        response.headers["hx-redirect"] = "/dashboard"
        return response


@router.post("/user/login")
async def user_login(request: Request, user: UserLogin) -> HTMLResponse: 
    response = await authenticate_user(user)
    if response["status"] == 200: 
        response = JSONResponse({"response": response["user_data"]})
        response.headers["hx-redirect"] = "/dashboard"
        return response
    else:
        raise HTTPException(status_code=response["status"], detail=response["message"])
