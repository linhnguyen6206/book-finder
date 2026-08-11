from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine
from routers import auth_router, books_router, favorites_router

# Create tables on startup (fine for SQLite / small apps; use Alembic migrations for production).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Card Catalog API",
    description="Backend for the Book Finder app - auth, favorites, search history, "
                 "and a Google Books proxy that keeps the API key server-side.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(books_router.router)
app.include_router(favorites_router.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
