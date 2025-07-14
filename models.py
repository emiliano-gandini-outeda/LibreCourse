from sqlalchemy import Column, String, Text, ForeignKey, Table, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from db import Base

# Many-to-many relationships
course_student = Table(
    "course_student", Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("course_id", UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String, default="student")
    avatar_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    enrolled_courses = relationship("Course", secondary=course_student, back_populates="students")
    created_courses = relationship("Course", back_populates="creator")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    
    @property
    def display_name(self):
        return f"{self.username}#{str(self.id)[:6]}"

class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False, index=True)
    description = Column(Text)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    category = Column(String)
    cover_url = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="active")
    students = relationship("User", secondary=course_student, back_populates="enrolled_courses")
    creator = relationship("User", back_populates="created_courses")
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    category_obj = relationship("Category", back_populates="courses")
    
class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"))
    course = relationship("Course", back_populates="lessons")
    notes = relationship("Note", back_populates="lesson", cascade="all, delete-orphan")
    
class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)  # Markdown text
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="notes")
    lesson = relationship("Lesson", back_populates="notes")
    
class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    courses = relationship("Course", back_populates="category_obj", cascade="all")
