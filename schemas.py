from pydantic import BaseModel, EmailStr
from uuid import UUID
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

class CourseCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    categoria: str | None = None

class CourseOut(BaseModel):
    id: UUID
    nombre: str
    descripcion: str | None
    fecha_creacion: datetime
    class Config:
        orm_mode = True