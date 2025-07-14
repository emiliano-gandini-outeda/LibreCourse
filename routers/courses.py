from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from schemas import CourseCreate, CourseOut, CourseUpdate
from models import User
import crud
from routers.auth import get_current_user
from db import get_db

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseOut)
def create_course(course: CourseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_course(db, current_user, course)

@router.get("/", response_model=List[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return crud.get_all_courses(db)

@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: UUID, db: Session = Depends(get_db)):
    course = crud.get_course_by_id(db, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=CourseOut)
def update_course(course_id: UUID, updates: CourseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated = crud.update_course(db, course_id, updates, current_user.id)
    if updated is None:
        raise HTTPException(status_code=403, detail="Not allowed to update this course")
    return updated

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = crud.delete_course(db, course_id, current_user.id)
    if not success:
        raise HTTPException(status_code=403, detail="Not allowed to delete this course")

@router.post("/{course_id}/enroll", status_code=status.HTTP_200_OK)
def enroll(course_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = crud.enroll_user_in_course(db, current_user, course_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not enroll or already enrolled")
    return {"message": "Enrolled successfully"}
