import os
import asyncpg
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv(f".env.{os.getenv('APP_ENV', 'local')}")
DATABASE_URL = os.getenv("DATABASE_URL")

async def connect_to_db():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database connection failed: {str(e)}")

async def setup_database():
    conn = await connect_to_db()
    try:
        await conn.execute('''CREATE SCHEMA IF NOT EXISTS api;''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS api.users (
            user_id VARCHAR(36) PRIMARY KEY,
            user_name VARCHAR(100) NOT NULL,
            user_display_name VARCHAR(100),
            user_email VARCHAR(100) NOT NULL UNIQUE,
            user_salt VARCHAR(255) NOT NULL,
            user_password VARCHAR(255) NOT NULL,
            user_disabled BOOLEAN DEFAULT FALSE,
            user_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''')
    finally:
        await conn.close()
