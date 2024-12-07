from pydantic import BaseModel, EmailStr, Field, validator

class UserLogin(BaseModel):
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=100)

    @validator("email", pre=True, always=True)
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email must not be empty.")
        return value
    
    @validator("password", pre=True, always=True)
    def validate_password(cls, value):
        if not value:
            raise ValueError("Password must not be empty.")
        return value