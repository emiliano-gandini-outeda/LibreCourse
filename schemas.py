from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# Base schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=1, max_length=50)
    role: Optional[str] = "student"
    avatar_url: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    avatar_url: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    role: str
    avatar_url: Optional[str]
    created_at: datetime
    display_name: str
    
    class Config:
        orm_mode = True

class UserPublic(BaseModel):
    id: UUID
    username: str
    avatar_url: Optional[str]
    display_name: str
    
    class Config:
        orm_mode = True

# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: UUID
    
    class Config:
        orm_mode = True

# Course schemas
class CourseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    cover_url: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    cover_url: Optional[str] = None
    status: Optional[str] = None

class CourseResponse(CourseBase):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    creator_id: UUID
    creator: UserPublic
    category: Optional[CategoryResponse]
    
    class Config:
        orm_mode = True

class CourseWithStudents(CourseResponse):
    students: List[UserPublic]
    
    class Config:
        orm_mode = True

# Lesson schemas
class LessonBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    content: Optional[str] = None

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    content: Optional[str] = None

class LessonResponse(LessonBase):
    id: UUID
    created_at: datetime
    course_id: UUID
    
    class Config:
        orm_mode = True

# Note schemas
class NoteBase(BaseModel):
    content: str = Field(..., min_length=1)

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)

class NoteResponse(NoteBase):
    id: UUID
    created_at: datetime
    user_id: UUID
    lesson_id: UUID
    user: UserPublic
    
    class Config:
        orm_mode = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
