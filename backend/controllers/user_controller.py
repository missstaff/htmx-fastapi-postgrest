import asyncpg
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from models.user.user_login import UserLogin
from models.user.user_create import UserCreate


environment = os.getenv("APP_ENV", "local") 
if environment == "production":
    env_file = ".env.prod" 
elif environment == "development":
    env_file = ".env.dev"
else:
    env_file = ".env.local"

load_dotenv(env_file)  
DATABASE_URL = os.getenv("DATABASE_URL") # second argument is an optional default value


async def create_user(user: UserCreate):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        user_data = await conn.execute(
            '''
            INSERT INTO api.users (name, display_name, email, password)
            VALUES ($1, $2, $3, $4)
            ''',
            user.name, user.display_name, user.email, user.password
        )
        await conn.close()

        if(user_data):
            return {
                'user_data': {
                    # "name": user.name,
                    "display_name": user.display_name,
                    "email": user.email
                },
                "status": 201,
                "message": "User created successfully"
            }
        else:
            raise HTTPException(status_code=400, detail="User creation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

async def authenticate_user(user: UserLogin):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        user_data = await conn.fetchrow(
            '''
            SELECT * FROM api.users WHERE email = $1 AND password = $2
            ''',
            user.email, user.password
        )
        await conn.close()

        if user_data:
            return {
                "user_data": {
                    # "id": user_data["id"],
                    # "name": user_data["name"],
                    "display_name": user_data["display_name"],
                    "email": user_data["email"],
                    # "created_at": user_data["created_at"]
                },
                "status": 200,
                "message": "User authenticated successfully"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")