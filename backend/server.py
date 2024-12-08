import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware 
from database import setup_database
from routes.app_routes import router as app_router
from routes.auth_routes import router as auth_router


load_dotenv(f".env.{os.getenv('APP_ENV', 'local')}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

    
@app.on_event("startup")
async def startup_event():
    await setup_database()
    print("Starting FastAPI server... http://127.0.0.1:8000")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down FastAPI server...")


app.include_router(app_router)
app.include_router(auth_router, tags=["auth"], prefix="/auth")
