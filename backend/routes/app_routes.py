from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


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