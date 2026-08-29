from pydantic import BaseModel, Field


class RegisterSchema(BaseModel):
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)
    role: str = Field(..., pattern="^(admin|candidate)$")


class LoginSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
