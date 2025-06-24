from fastapi import APIRouter, Depends, HTTPException, status, Request

from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.user import get_user_by_email
from app.core.security import verify_password
from app.core.token import create_access_token



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login",)
def login(
    db: Session = Depends(get_db),
    user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(db, user_credentials.username)
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

