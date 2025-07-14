from sqlalchemy.orm import Session
from models import User, Course
from schemas import UserCreate, CourseCreate, CourseUpdate
from routers.auth import hash_password, verify_password
from datetime import datetime, timezone
from uuid import UUID

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_pw = hash_password(user.password)
    new_user = User(
        email=user.email,
        username=user.username,
        password_hash=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_course(db: Session, user: User, course_data: CourseCreate) -> Course:
    new_course = Course(
        name=course_data.name,
        description=course_data.description,
        cover_url=course_data.cover_url,
        creator_id=user.id,
        category_id=course_data.category_id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

def get_all_courses(db: Session) -> list[Course]:
    return db.query(Course).all()

def get_course_by_id(db: Session, course_id: UUID) -> Course | None:
    return db.query(Course).filter(Course.id == course_id).first()

def update_course(db: Session, course_id: UUID, updates: CourseUpdate, user_id: UUID) -> Course | None:
    course = db.query(Course).filter(Course.id == course_id, Course.creator_id == user_id).first()
    if course is None:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(course, key, value)
    course.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(course)
    return course

def delete_course(db: Session, course_id: UUID, user_id: UUID) -> bool:
    course = db.query(Course).filter(Course.id == course_id, Course.creator_id == user_id).first()
    if course is None:
        return False
    db.delete(course)
    db.commit()
    return True

def enroll_user_in_course(db: Session, user: User, course_id: UUID) -> bool:
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None or user in course.students:
        return False
    course.students.append(user)
    db.commit()
    return True
