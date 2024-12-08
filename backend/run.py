import os
import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    host = "0.0.0.0" 
    port = 8000

    load_dotenv(f".env.{os.getenv('APP_ENV', 'local')}")
    environment = os.getenv("APP_ENV", "local") 

    if environment == "production":
        uvicorn.run("server:app", host=host, port=port, workers=4)
    else:
        uvicorn.run("server:app", host=host, port=port, reload=True)

