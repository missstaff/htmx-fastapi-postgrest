import asyncpg
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv(f".env.{os.getenv('APP_ENV', 'local')}")
DATABASE_URL = os.getenv("DATABASE_URL")

async def connect_to_db():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

async def setup_database():
    conn = await connect_to_db()
    try:
        await conn.execute('''CREATE SCHEMA IF NOT EXISTS api;''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS api.users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            display_name VARCHAR(100),
            email VARCHAR(100) NOT NULL UNIQUE,
            salt VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            disabled BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''')
    finally:
        await conn.close()
