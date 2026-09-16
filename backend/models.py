from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String,)
from sqlalchemy.orm import relationship

from backend.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    completed = Column(
        Boolean,
        default=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    owner = relationship(
        "User",
        back_populates="tasks"
    )


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    tasks = relationship(
        "Task",
        back_populates="owner"
    )

