from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from models import Category
from schemas import CategoryOut
from db import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
