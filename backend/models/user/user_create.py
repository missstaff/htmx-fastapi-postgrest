from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(None, min_length=1, max_length=100)
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=100)

    @validator("name", pre=True, always=True)
    def validate_name(cls, value):
        if value is None or not value.strip():
            raise ValueError("Name must not be empty.")
        return value

    @validator("email", pre=True, always=True)
    def validate_email(cls, value):
        if value is None or not value:
            raise ValueError("Email must not be empty.")
        return value
    
    @validator("password", pre=True, always=True)
    def validate_password(cls, value):
        if value is None or not value:
            raise ValueError("Password must not be empty.")
        return value
    
    @validator("display_name", pre=True, always=True)
    def validate_display_name(cls, value):
        if value is None or not value.strip():  
            raise ValueError("Display name must not be empty.")
        return value

