import jwt

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from backend import crud
from backend.database import get_db
from backend.security import decode_access_token


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )

        user_id = int(user_id)

    except (
        jwt.InvalidTokenError,
        ValueError
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )

    user = crud.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )

    return user

