from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from ..schemas import LessonCreate, LessonUpdate, LessonResponse
from ..security import get_current_user
from ..crud import (
    get_lessons_by_course,
    get_lesson_by_id,
    create_lesson,
    update_lesson,
    delete_lesson,
    get_course_by_id
)
from ..models import User

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.get("/courses/{course_id}/lessons", response_model=List[LessonResponse])
def list_course_lessons(
    course_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get list of lessons for a specific course.
    
    - **course_id**: Course ID
    - **skip**: Number of lessons to skip (for pagination)
    - **limit**: Maximum number of lessons to return (1-100)
    """
    # Verify course exists
    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    lessons = get_lessons_by_course(db, course_id, skip=skip, limit=limit)
    return lessons

@router.post("/courses/{course_id}/lessons", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def create_course_lesson(
    course_id: UUID,
    lesson: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new lesson in a course.
    
    Only the course creator can add lessons.
    
    - **title**: Lesson title (required)
    - **description**: Lesson description (optional)
    - **content**: Lesson content in Markdown format (optional)
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
            detail="Not authorized to create lessons in this course"
        )
    
    db_lesson = create_lesson(db, lesson, course_id)
    return db_lesson

@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson_details(lesson_id: UUID, db: Session = Depends(get_db)):
    """
    Get detailed lesson information.
    """
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    return lesson

@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson_info(
    lesson_id: UUID,
    lesson_update: LessonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update lesson information.
    
    Only the course creator can update lessons.
    """
    # Check if lesson exists and user is the course creator
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    if lesson.course.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this lesson"
        )
    
    updated_lesson = update_lesson(db, lesson_id, lesson_update)
    return updated_lesson

@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson_by_id(
    lesson_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a lesson.
    
    Only the course creator can delete lessons.
    This will cascade delete all notes associated with the lesson.
    """
    # Check if lesson exists and user is the course creator
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    if lesson.course.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this lesson"
        )
    
    delete_lesson(db, lesson_id)
