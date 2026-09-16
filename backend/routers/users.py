from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.auth import get_current_user
from backend.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=201
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = crud.get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return crud.create_user(
        db,
        user
    )


@router.get(
    "/me",
    response_model=schemas.UserResponse
)
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user

