from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow)

    favorites = relationship("Favorite", back_populates="owner", cascade="all, delete-orphan")
    search_history = relationship("SearchHistory", back_populates="owner", cascade="all, delete-orphan")


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "google_books_id", name="uq_user_book"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    google_books_id = Column(String(64), nullable=False)
    title = Column(String(512), nullable=False)
    authors = Column(String(512), default="")
    thumbnail = Column(String(1024), default="")
    published_date = Column(String(32), default="")
    info_link = Column(String(1024), default="")
    added_at = Column(DateTime(timezone=True), default=utcnow)

    owner = relationship("User", back_populates="favorites")


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query = Column(String(512), nullable=False)
    result_count = Column(Integer, default=0)
    searched_at = Column(DateTime(timezone=True), default=utcnow)

    owner = relationship("User", back_populates="search_history")
