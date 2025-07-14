from sqlalchemy.orm import Session
from models import Usuario
from schemas import UserCreate
from routers.auth import hash_password, verify_password

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