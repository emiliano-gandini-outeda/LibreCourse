from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..database import get_db
from ..schemas import CourseCreate, CourseUpdate, CourseResponse, CourseWithStudents
from ..security import get_current_user
from ..crud import (
    get_courses,
    get_course_by_id,
    create_course,
    update_course,
    delete_course,
    enroll_user_in_course,
    unenroll_user_from_course
)
from ..models import User

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=List[CourseResponse])
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category_id: Optional[UUID] = Query(None),
    creator_id: Optional[UUID] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get list of courses with optional filters.
    
    - **skip**: Number of courses to skip (for pagination)
    - **limit**: Maximum number of courses to return (1-100)
    - **category_id**: Filter by category ID
    - **creator_id**: Filter by creator user ID
    - **search**: Search in course name and description
    """
    courses = get_courses(
        db, 
        skip=skip, 
        limit=limit,
        category_id=category_id,
        creator_id=creator_id,
        search=search
    )
    return courses

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_new_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new course.
    
    Requires authentication. The authenticated user becomes the course creator.
    
    - **name**: Course name (required)
    - **description**: Course description (optional)
    - **category_id**: Category ID (optional)
    - **cover_url**: Cover image URL (optional)
    """
    db_course = create_course(db, course, current_user.id)
    return get_course_by_id(db, db_course.id)

@router.get("/{course_id}", response_model=CourseWithStudents)
def get_course_details(course_id: UUID, db: Session = Depends(get_db)):
    """
    Get detailed course information including enrolled students.
    """
    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course_info(
    course_id: UUID,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update course information.
    
    Only the course creator can update the course.
    """
    # Check if course exists and user is the creator
    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this course"
        )
    
    updated_course = update_course(db, course_id, course_update)
    return get_course_by_id(db, updated_course.id)

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_by_id(
    course_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a course.
    
    Only the course creator can delete the course.
    This will cascade delete all lessons and notes associated with the course.
    """
    # Check if course exists and user is the creator
    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this course"
        )
    
    delete_course(db, course_id)

@router.post("/{course_id}/enroll", status_code=status.HTTP_200_OK)
def enroll_in_course(
    course_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Enroll current user in a course.
    """
    if not enroll_user_in_course(db, current_user.id, course_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not enroll in course (course not found or already enrolled)"
        )
    
    return {"message": "Successfully enrolled in course"}

@router.post("/{course_id}/unenroll", status_code=status.HTTP_200_OK)
def unenroll_from_course(
    course_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Unenroll current user from a course.
    """
    if not unenroll_user_from_course(db, current_user.id, course_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not unenroll from course (course not found or not enrolled)"
        )
    
    return {"message": "Successfully unenrolled from course"}
