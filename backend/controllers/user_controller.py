import asyncpg
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from models.user.user_login import UserLogin
from models.user.user_hashed import UserCreateHashed, UserLoginHashed
import bcrypt

environment = os.getenv("APP_ENV", "local")
dotenv_file = f".env.{environment}" 
load_dotenv(dotenv_file)

DATABASE_URL = os.getenv("DATABASE_URL") 

async def create_user(user: UserCreateHashed):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("in controller", user)
        user_data = await conn.execute(
            '''
            INSERT INTO api.users (name, display_name, email, salt, password)
            VALUES ($1, $2, $3, $4, $5)
            ''',
            user.name, user.display_name, user.email, user.salt, user.hash_password
        )
        await conn.close()

        if(user_data):
            return {
                'user_data': {
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
            SELECT * FROM api.users WHERE email = $1
            ''',
            user.email
        )
        await conn.close()
        if user_data:
                userBytes = user.password.encode('utf-8') 
                if(bcrypt.checkpw(userBytes, user_data["password"].encode('utf-8'))):
                    return {
                        "user_data": {
                            "display_name": user_data["display_name"],
                            "email": user_data["email"],
                        },
                        "status": 200,
                        "message": "User authenticated successfully"
                    }
                else:
                    raise HTTPException(status_code=401, detail="User not found! Invalid email or password.")
        else:
            raise HTTPException(status_code=401, detail="User not found! Invalid email or password.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")