
import os
import jwt
import uuid
import asyncpg
import bcrypt
from dotenv import load_dotenv
from fastapi import HTTPException
from models.user.user_login import UserLogin
from models.user.user_hashed import UserCreateHashed

environment = os.getenv("APP_ENV", "local")
dotenv_file = f".env.{environment}" 
load_dotenv(dotenv_file)

DATABASE_URL = os.getenv("DATABASE_URL") 
ALGORITHM = os.getenv("ALGORITHM")
JWT_KEY = os.getenv("JWT_KEY")
EXPIRATION_TIME = os.getenv("EXPIRATION_TIME")

async def create_user(user: UserCreateHashed):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        user_id = str(uuid.uuid4())
        user_data = await conn.execute(
            '''
            INSERT INTO api.users (user_name, user_display_name, user_email, user_salt, user_password, user_id)
            VALUES ($1, $2, $3, $4, $5, $6)
            ''',
            user.name, user.display_name, user.email, user.salt, user.hash_password, user_id
        )
        await conn.close()
        if(user_data):
            token = jwt.encode({"user_id": user_id, "user_name": user.display_name}, JWT_KEY, ALGORITHM)
            response =  {
                'user_data': {
                    "display_name": user.display_name,
                    "email": user.email,
                    "disabled": False
                },
                "status": 201,
                "message": "User created successfully",
                "access_token": token
            }
            return response
        else:
            raise HTTPException(status_code=400, detail="User creation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


async def authenticate_user(user: UserLogin):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        user_data = await conn.fetchrow(
            '''
            SELECT * FROM api.users WHERE user_email = $1
            ''',
            user.email
        )
        await conn.close()
        if user_data:
                userBytes = user.password.encode('utf-8') 
                if(bcrypt.checkpw(userBytes, user_data["user_password"].encode('utf-8'))):
                    token = jwt.encode({"user_id": user_data["user_id"], "user_name": user_data["user_display_name"]}, JWT_KEY, ALGORITHM)
                    response ={
                        "user_data": {
                            "display_name": user_data["user_display_name"],
                            "email": user_data["user_email"],
                            "disabled": user_data["user_disabled"]
                        },
                        "status": 200,
                        "message": "User authenticated successfully",
                        "access_token": token
                    }
                    return response
                else:
                    raise HTTPException(status_code=400, detail="Passwords do not match.")
        else:
            raise HTTPException(status_code=401, detail="User not found! Invalid email or password.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")