from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from auth import get_current_user

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


@router.get("", response_model=list[schemas.FavoriteOut])
def list_favorites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Favorite)
        .filter(models.Favorite.user_id == current_user.id)
        .order_by(models.Favorite.added_at.desc())
        .all()
    )


@router.post("", response_model=schemas.FavoriteOut, status_code=201)
def add_favorite(
    payload: schemas.FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    favorite = models.Favorite(user_id=current_user.id, **payload.model_dump())
    db.add(favorite)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="That book is already in your favorites")
    db.refresh(favorite)
    return favorite


@router.delete("/{favorite_id}", status_code=204)
def remove_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    favorite = (
        db.query(models.Favorite)
        .filter(models.Favorite.id == favorite_id, models.Favorite.user_id == current_user.id)
        .first()
    )
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(favorite)
    db.commit()
