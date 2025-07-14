from pydantic import BaseModel, EmailStr, UUID4
from uuid import UUID
from typing import Optional, List
from datetime import datetime, timezone

# Request body for user registration
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

# Request body for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Response model for user info (no password)
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str

    class Config:
        orm_mode = True

# Response model for token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryOut(CategoryBase):
    id: UUID4

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    cover_url: Optional[str] = None

class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    cover_url: Optional[str] = None
    category_id: Optional[UUID4] = None

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    cover_url: Optional[str] = None

class CourseOut(BaseModel):
    id: UUID4
    name: str
    description: Optional[str]
    cover_url: Optional[str]
    status: str
    creator_id: UUID4
    category_obj: Optional[CategoryOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
