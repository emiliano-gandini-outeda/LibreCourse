from sqlalchemy.orm import Session
from models import Usuario, Curso
from schemas import UserCreate, CourseCreate, CourseUpdate
from routers.auth import hash_password, verify_password
from datetime import datetime, timezone
from uuid import UUID

def get_user_by_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()

def create_user(db: Session, user: UserCreate) -> Usuario:
    hashed_pw = hash_password(user.password)
    new_user = Usuario(
        email=user.email,
        username=user.username,
        password_hash=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: str, password: str) -> Usuario | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_course(db: Session, user: Usuario, course_data: CourseCreate) -> Curso:
    new_course = Curso(
        nombre=course_data.nombre,
        descripcion=course_data.descripcion,
        categoria=course_data.categoria,
        portada_url=course_data.portada_url,
        creador_id=user.id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

def get_all_courses(db: Session) -> list[Curso]:
    return db.query(Curso).all()

def get_course_by_id(db: Session, course_id: UUID) -> Curso | None:
    return db.query(Curso).filter(Curso.id == course_id).first()

def update_course(db: Session, course_id: UUID, updates: CourseUpdate, user_id: UUID) -> Curso | None:
    course = db.query(Curso).filter(Curso.id == course_id, Curso.creador_id == user_id).first()
    if course is None:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(course, key, value)
    course.ultima_actualizacion = datetime.now(timezone.utc)
    db.commit()
    db.refresh(course)
    return course

def delete_course(db: Session, course_id: UUID, user_id: UUID) -> bool:
    course = db.query(Curso).filter(Curso.id == course_id, Curso.creador_id == user_id).first()
    if course is None:
        return False
    db.delete(course)
    db.commit()
    return True

def enroll_user_in_course(db: Session, user: Usuario, course_id: UUID) -> bool:
    course = db.query(Curso).filter(Curso.id == course_id).first()
    if course is None or user in course.estudiantes:
        return False
    course.estudiantes.append(user)
    db.commit()
    return True