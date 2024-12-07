import os
import asyncpg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
    context = {
        "request": request,
    }
    return templates.TemplateResponse("index.html", context=context)


app.include_router(app_router)
app.include_router(auth_router, tags=["auth"], prefix="/auth")
