from sqlalchemy import Column, String, Text, ForeignKey, Table, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from db import Base

# Many-to-many relationships
curso_estudiante = Table(
    "curso_estudiante", Base.metadata,
    Column("usuario_id", UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True),
    Column("curso_id", UUID(as_uuid=True), ForeignKey("cursos.id", ondelete="CASCADE"), primary_key=True)
)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), nullable=False)
    password_hash = Column(Text, nullable=False)
    rol = Column(String, default="estudiante")
    avatar_url = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    cursos_inscriptos = relationship("Curso", secondary=curso_estudiante, back_populates="estudiantes")
    cursos_creados = relationship("Curso", back_populates="creador")
    notas = relationship("Nota", back_populates="usuario", cascade="all, delete-orphan")
    @property
    def display_name(self):
        return f"{self.username}#{str(self.id)[:6]}"

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(Text, nullable=False, index=True)
    descripcion = Column(Text)
    creador_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    categoria = Column(String)
    portada_url = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ultima_actualizacion = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    estado = Column(String, default="activo")
    estudiantes = relationship("Usuario", secondary=curso_estudiante)
    creador = relationship("Usuario", back_populates="cursos_creados")
    lecciones = relationship("Leccion", back_populates="curso", cascade="all, delete-orphan")
    
class Leccion(Base):
    __tablename__ = "lecciones"
    
    id = Column(UUID(as_uuid=True), primary_key = True, default = uuid.uuid4)
    titulo = Column(Text, nullable=False)
    descripcion = Column(Text)
    contenido = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    curso_id = Column(UUID(as_uuid=True), ForeignKey("cursos.id", ondelete="CASCADE"))
    curso = relationship("Curso", back_populates="lecciones")
    notas = relationship("Nota", back_populates="leccion", cascade="all, delete-orphan")
    
class Nota(Base):
    __tablename__ = "notas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contenido = Column(Text, nullable=False)  # Texto en Markdown
    fecha_creacion = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"))
    leccion_id = Column(UUID(as_uuid=True), ForeignKey("lecciones.id", ondelete="CASCADE"))
    usuario = relationship("Usuario", back_populates="notas")
    leccion = relationship("Leccion", back_populates="notas")