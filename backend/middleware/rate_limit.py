import os
import logging
from datetime import datetime, timedelta
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from httpx import AsyncClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgREST URL
POSTGREST_URL = os.getenv("POSTGREST_URL", "http://localhost:3000/rate_limit")

# Rate limit configuration
RATE_LIMIT = 100  # Max requests per minute
TIME_WINDOW = timedelta(minutes=1)  # 1 minute time window

# Logging setup
environment = os.getenv("APP_ENV", "development")  # Default to 'development' if not set
logger = logging.getLogger(__name__)
if environment == "development":
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.ERROR)

# Use an async client for HTTP requests
client = AsyncClient()

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ip = request.client.host
        try:
            # Query PostgREST to get rate limit info for the current IP
            rate_limit_data = await self.get_rate_limit(ip)
            
            # Check if it’s been more than the time window
            last_request_time = datetime.fromisoformat(rate_limit_data["last_request_time"])
            if datetime.utcnow() - last_request_time > TIME_WINDOW:
                # Reset the request count if the time window has passed
                await self.reset_rate_limit(ip)
                response = await call_next(request)
                return response

            # If the request count exceeds the rate limit
            if rate_limit_data["request_count"] >= RATE_LIMIT:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            # Increment request count and update last request time
            await self.increment_rate_limit(ip, rate_limit_data["request_count"])

        except Exception as e:
            logger.error(f"Error with rate limiter: {e}")
            raise HTTPException(status_code=500, detail="Internal server error with rate limit service")

        response = await call_next(request)
        return response

    async def get_rate_limit(self, ip: str):
        """Fetch rate limit data from PostgREST."""
        try:
            response = await client.get(f"{POSTGREST_URL}?ip_address=eq.{ip}")
            response.raise_for_status()
            # If IP not found, create a new record
            if not response.json():
                return await self.create_rate_limit_record(ip)
            return response.json()[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get rate limit data: {e}")

    async def create_rate_limit_record(self, ip: str):
        """Create a new rate limit record for a new IP."""
        data = {
            "ip_address": ip,
            "request_count": 1,
            "last_request_time": datetime.utcnow().isoformat()
        }
        response = await client.post(POSTGREST_URL, json=data)
        response.raise_for_status()
        return response.json()[0]

    async def reset_rate_limit(self, ip: str):
        """Reset the rate limit data after the time window has passed."""
        data = {"request_count": 1, "last_request_time": datetime.utcnow().isoformat()}
        await client.patch(f"{POSTGREST_URL}?ip_address=eq.{ip}", json=data)

    async def increment_rate_limit(self, ip: str, current_count: int):
        """Increment the rate limit counter."""
        data = {"request_count": current_count + 1, "last_request_time": datetime.utcnow().isoformat()}
        await client.patch(f"{POSTGREST_URL}?ip_address=eq.{ip}", json=data)
