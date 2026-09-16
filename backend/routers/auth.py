from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.database import get_db
from backend.security import create_access_token


router = APIRouter(
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=schemas.TokenResponse
)
def login(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(
        db,
        credentials.email,
        credentials.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

