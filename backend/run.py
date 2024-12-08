import os
from dotenv import load_dotenv
import uvicorn


if __name__ == "__main__":
    host = "0.0.0.0" 
    port = 8000

    environment = os.getenv("APP_ENV", "local")
    dotenv_file = f".env.{environment}" 
    load_dotenv(dotenv_file)
    environment = os.getenv("APP_ENV", "local") 

    if environment == "production":
        uvicorn.run("server:app", host=host, port=port, workers=4)
    else:
        uvicorn.run("server:app", host=host, port=port, reload=True)

