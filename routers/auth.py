from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from ..schemas import UserCreate, UserResponse, Token, LoginRequest
from ..security import (
    authenticate_user, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..crud import create_user, get_user_by_email
from ..models import User
from ..rate_limiter import login_rate_limiter

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    - **email**: Valid email address (must be unique)
    - **username**: Username (1-50 characters, non-unique allowed)
    - **password**: Password (minimum 8 characters)
    """
    # Check if user already exists
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = create_user(db, user)
    return db_user

@router.post("/login", response_model=Token)
def login(
    request: Request,
    login_data: LoginRequest, 
    db: Session = Depends(get_db),
    _: None = Depends(login_rate_limiter)
):
    """
    Authenticate user and return JWT access token.
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns JWT token that expires in 24 hours by default.
    """
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Requires valid JWT token in Authorization header.
    """
    return current_user
