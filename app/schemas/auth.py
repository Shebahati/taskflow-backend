from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: str = Field(min_length=2, max_length=80)

class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
