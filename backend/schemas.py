from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Books ----------

class BookResult(BaseModel):
    google_books_id: str
    title: str
    authors: str
    published_date: str
    thumbnail: str | None = None
    description: str
    info_link: str
    categories: str | None = None
    page_count: int | None = None
    average_rating: float | None = None


class SearchResponse(BaseModel):
    query: str
    total_items: int
    items: list[BookResult]


class SearchHistoryOut(BaseModel):
    id: int
    query: str
    result_count: int
    searched_at: datetime

    class Config:
        from_attributes = True


# ---------- Favorites ----------

class FavoriteCreate(BaseModel):
    google_books_id: str
    title: str
    authors: str = ""
    thumbnail: str = ""
    published_date: str = ""
    info_link: str = ""


class FavoriteOut(BaseModel):
    id: int
    google_books_id: str
    title: str
    authors: str
    thumbnail: str
    published_date: str
    info_link: str
    added_at: datetime

    class Config:
        from_attributes = True
