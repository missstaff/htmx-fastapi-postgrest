from pydantic import BaseModel

class UserCreateHashed(BaseModel):
    name: str
    display_name: str
    email: str 
    salt: str
    hash_password: str