from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"

class TaskStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole,nullable=False, default=UserRole.USER))

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=False)
    status = Column(Enum(TaskStatus, nullable=False, default=TaskStatus.PENDING))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="tasks")
