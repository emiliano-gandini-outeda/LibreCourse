from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from models import Categoria
from schemas import CategoriaOut
from db import get_db

router = APIRouter(prefix="/categories",tags=["Categories"])

@router.get("/categories", response_model=List[CategoriaOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Categoria).all()