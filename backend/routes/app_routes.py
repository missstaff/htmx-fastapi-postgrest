from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from auth.access_token_utils import verify_jwt_token


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request) -> HTMLResponse:
    context = {
    "request": request,
    }
    return templates.TemplateResponse("signup.html", context=context)


@router.get("/signin", response_class=HTMLResponse)
async def signin(request: Request) -> HTMLResponse:
    context = {
    "request": request,
    }
    return templates.TemplateResponse("signin.html", context=context)


@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request) -> HTMLResponse:
    access_token = request.cookies.get("access_token")
    if access_token:
        user_data = verify_jwt_token(access_token)
        if user_data:
            context = {
                "request": request,
                "user": user_data
            }
            return templates.TemplateResponse("index.html", context=context)
        else:
            return RedirectResponse("/signin", status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/signin", status.HTTP_303_SEE_OTHER)