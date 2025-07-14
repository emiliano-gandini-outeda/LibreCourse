from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from ..security import get_current_admin_user
from ..crud import (
    get_categories, 
    get_category_by_id, 
    get_category_by_name,
    create_category, 
    update_category, 
    delete_category
)
from ..models import User

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryResponse])
def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get list of all categories.
    
    - **skip**: Number of categories to skip (for pagination)
    - **limit**: Maximum number of categories to return (1-100)
    """
    categories = get_categories(db, skip=skip, limit=limit)
    return categories

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Create a new category.
    
    Requires admin role.
    
    - **name**: Category name (must be unique)
    - **description**: Optional category description
    """
    # Check if category name already exists
    if get_category_by_name(db, category.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )
    
    return create_category(db, category)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_info(
    category_id: UUID,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Update category information.
    
    Requires admin role.
    """
    # Check if new name already exists (if name is being updated)
    if category_update.name:
        existing_category = get_category_by_name(db, category_update.name)
        if existing_category and existing_category.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists"
            )
    
    updated_category = update_category(db, category_id, category_update)
    if not updated_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return updated_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_by_id(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete a category.
    
    Requires admin role.
    This will set category_id to NULL for all courses in this category.
    """
    if not delete_category(db, category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
