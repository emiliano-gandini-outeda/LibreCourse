from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone

from .models import User, Category, Course, Lesson, Note
from .schemas import (
    UserCreate, UserUpdate,
    CategoryCreate, CategoryUpdate,
    CourseCreate, CourseUpdate,
    LessonCreate, LessonUpdate,
    NoteCreate, NoteUpdate
)
from .security import get_password_hash

# User CRUD operations
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: UUID) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# Category CRUD operations
def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

def get_category_by_id(db: Session, category_id: UUID) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    return db.query(Category).filter(Category.name == name).first()

def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: UUID, category_update: CategoryUpdate) -> Optional[Category]:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: UUID) -> bool:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return False
    
    db.delete(db_category)
    db.commit()
    return True

# Course CRUD operations
def get_courses(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[UUID] = None,
    creator_id: Optional[UUID] = None,
    search: Optional[str] = None
) -> List[Course]:
    query = db.query(Course).options(
        joinedload(Course.creator),
        joinedload(Course.category)
    )
    
    if category_id:
        query = query.filter(Course.category_id == category_id)
    
    if creator_id:
        query = query.filter(Course.creator_id == creator_id)
    
    if search:
        query = query.filter(
            or_(
                Course.name.ilike(f"%{search}%"),
                Course.description.ilike(f"%{search}%")
            )
        )
    
    return query.offset(skip).limit(limit).all()

def get_course_by_id(db: Session, course_id: UUID) -> Optional[Course]:
    return db.query(Course).options(
        joinedload(Course.creator),
        joinedload(Course.category),
        joinedload(Course.students)
    ).filter(Course.id == course_id).first()

def create_course(db: Session, course: CourseCreate, creator_id: UUID) -> Course:
    db_course = Course(**course.dict(), creator_id=creator_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, course_id: UUID, course_update: CourseUpdate) -> Optional[Course]:
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        return None
    
    update_data = course_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    db_course.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: UUID) -> bool:
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        return False
    
    db.delete(db_course)
    db.commit()
    return True

def enroll_user_in_course(db: Session, user_id: UUID, course_id: UUID) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not user or not course:
        return False
    
    if course in user.enrolled_courses:
        return False  # Already enrolled
    
    user.enrolled_courses.append(course)
    db.commit()
    return True

def unenroll_user_from_course(db: Session, user_id: UUID, course_id: UUID) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not user or not course:
        return False
    
    if course not in user.enrolled_courses:
        return False  # Not enrolled
    
    user.enrolled_courses.remove(course)
    db.commit()
    return True

# Lesson CRUD operations
def get_lessons_by_course(db: Session, course_id: UUID, skip: int = 0, limit: int = 100) -> List[Lesson]:
    return db.query(Lesson).filter(Lesson.course_id == course_id).offset(skip).limit(limit).all()

def get_lesson_by_id(db: Session, lesson_id: UUID) -> Optional[Lesson]:
    return db.query(Lesson).options(joinedload(Lesson.course)).filter(Lesson.id == lesson_id).first()

def create_lesson(db: Session, lesson: LessonCreate, course_id: UUID) -> Lesson:
    db_lesson = Lesson(**lesson.dict(), course_id=course_id)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def update_lesson(db: Session, lesson_id: UUID, lesson_update: LessonUpdate) -> Optional[Lesson]:
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not db_lesson:
        return None
    
    update_data = lesson_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_lesson, field, value)
    
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def delete_lesson(db: Session, lesson_id: UUID) -> bool:
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not db_lesson:
        return False
    
    db.delete(db_lesson)
    db.commit()
    return True

# Note CRUD operations
def get_notes_by_lesson(db: Session, lesson_id: UUID, skip: int = 0, limit: int = 100) -> List[Note]:
    return db.query(Note).options(joinedload(Note.user)).filter(Note.lesson_id == lesson_id).offset(skip).limit(limit).all()

def get_note_by_id(db: Session, note_id: UUID) -> Optional[Note]:
    return db.query(Note).options(joinedload(Note.user)).filter(Note.id == note_id).first()

def create_note(db: Session, note: NoteCreate, lesson_id: UUID, user_id: UUID) -> Note:
    db_note = Note(**note.dict(), lesson_id=lesson_id, user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: UUID, note_update: NoteUpdate) -> Optional[Note]:
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        return None
    
    update_data = note_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_note, field, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: UUID) -> bool:
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        return False
    
    db.delete(db_note)
    db.commit()
    return True
