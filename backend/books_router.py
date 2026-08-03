import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import models
import schemas
from config import settings
from database import get_db
from auth import get_current_user, get_current_user_optional

router = APIRouter(prefix="/api/books", tags=["books"])

GOOGLE_BOOKS_ENDPOINT = "https://www.googleapis.com/books/v1/volumes"


def _to_book_result(item: dict) -> schemas.BookResult:
    info = item.get("volumeInfo", {})
    image_links = info.get("imageLinks", {})
    thumbnail = image_links.get("thumbnail") or image_links.get("smallThumbnail")
    if thumbnail:
        thumbnail = thumbnail.replace("http://", "https://")

    return schemas.BookResult(
        google_books_id=item.get("id", ""),
        title=info.get("title", "Untitled"),
        authors=", ".join(info.get("authors", [])) or "Unknown author",
        published_date=info.get("publishedDate", ""),
        thumbnail=thumbnail,
        description=info.get("description", "No description available for this edition."),
        info_link=info.get("infoLink", ""),
        categories=(info.get("categories") or [None])[0],
        page_count=info.get("pageCount"),
        average_rating=info.get("averageRating"),
    )


@router.get("/search", response_model=schemas.SearchResponse)
async def search_books(
    q: str = Query(..., min_length=1, description="Search query - title, author, subject, etc."),
    max_results: int = Query(20, ge=1, le=40),
    db: Session = Depends(get_db),
    current_user: models.User | None = Depends(get_current_user_optional),
):
    """
    Proxies the Google Books API. The API key lives only in the server's
    environment (config.settings) and is never sent to the browser.
    If the caller is authenticated, the query is saved to their search history.
    """
    params = {"q": q, "maxResults": max_results}
    if settings.google_books_api_key:
        params["key"] = settings.google_books_api_key

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(GOOGLE_BOOKS_ENDPOINT, params=params)
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Google Books API error: {exc}")

    data = resp.json()
    raw_items = data.get("items", [])
    items = [_to_book_result(item) for item in raw_items]

    if current_user is not None:
        db.add(models.SearchHistory(user_id=current_user.id, query=q, result_count=len(items)))
        db.commit()

    return schemas.SearchResponse(query=q, total_items=data.get("totalItems", 0), items=items)


@router.get("/history", response_model=list[schemas.SearchHistoryOut])
def get_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.SearchHistory)
        .filter(models.SearchHistory.user_id == current_user.id)
        .order_by(models.SearchHistory.searched_at.desc())
        .limit(50)
        .all()
    )


@router.delete("/history/{history_id}", status_code=204)
def delete_history_item(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = (
        db.query(models.SearchHistory)
        .filter(models.SearchHistory.id == history_id, models.SearchHistory.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="History entry not found")
    db.delete(item)
    db.commit()


@router.delete("/history", status_code=204)
def clear_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db.query(models.SearchHistory).filter(models.SearchHistory.user_id == current_user.id).delete()
    db.commit()
