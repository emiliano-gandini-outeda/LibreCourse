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

class CourseBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    portada_url: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    categoria: Optional[str]
    portada_url: Optional[str]

class CourseOut(CourseBase):
    id: UUID4
    creador_id: UUID4
    fecha_creacion: datetime
    ultima_actualizacion: datetime
    estado: str

    class Config:
        orm_mode = True