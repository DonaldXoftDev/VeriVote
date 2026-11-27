from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import UserRole


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8,)
    org_name: str


class UserLogin(UserBase):
    password: str = Field(..., min_length=8,)

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    org_name: str| None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str =  'bearer'
    user: UserResponse

class LogoutUser(BaseModel):
    message: str = "Logged out successfully"
