from sqlalchemy import Column, String, Text, ForeignKey, Table, DateTime, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone
import uuid
from .database import Base

# Many-to-many relationship table for course enrollment
course_student = Table(
    "course_student", 
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("course_id", UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
    Index("idx_course_student_user", "user_id"),
    Index("idx_course_student_course", "course_id")
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), default="student", nullable=False)
    avatar_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    enrolled_courses = relationship("Course", secondary=course_student, back_populates="students")
    created_courses = relationship("Course", back_populates="creator", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    
    @property
    def display_name(self):
        return f"{self.username}#{str(self.id)[:6]}"
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    courses = relationship("Course", back_populates="category", cascade="all")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    cover_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(String(20), default="active", nullable=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    category = relationship("Category", back_populates="courses")
    creator = relationship("User", back_populates="created_courses")
    students = relationship("User", secondary=course_student, back_populates="enrolled_courses")
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index("idx_course_name", "name"),
        Index("idx_course_creator", "creator_id"),
        Index("idx_course_category", "category_id"),
        Index("idx_course_status", "status"),
    )
    
    def __repr__(self):
        return f"<Course(id={self.id}, name={self.name}, creator_id={self.creator_id})>"

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Markdown content
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    course = relationship("Course", back_populates="lessons")
    notes = relationship("Note", back_populates="lesson", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index("idx_lesson_course", "course_id"),
    )
    
    def __repr__(self):
        return f"<Lesson(id={self.id}, title={self.title}, course_id={self.course_id})>"

class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)  # Markdown content
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="notes")
    lesson = relationship("Lesson", back_populates="notes")
    
    # Indexes
    __table_args__ = (
        Index("idx_note_user", "user_id"),
        Index("idx_note_lesson", "lesson_id"),
    )
    
    def __repr__(self):
        return f"<Note(id={self.id}, user_id={self.user_id}, lesson_id={self.lesson_id})>"
