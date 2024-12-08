import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from auth.access_token_utils import verify_jwt_token
from database import setup_database
from routes.app_routes import router as app_router
from routes.auth_routes import router as auth_router


app = FastAPI()


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


environment = os.getenv("APP_ENV", "local")
dotenv_file = f".env.{environment}" 
load_dotenv(dotenv_file)

    
@app.on_event("startup")
async def startup_event():
    await setup_database()
    print("Starting FastAPI server... http://127.0.0.1:8000")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down FastAPI server...")


@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
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


app.include_router(app_router)
app.include_router(auth_router, tags=["auth"], prefix="/auth")
