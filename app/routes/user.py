from app.api.deps import get_db
from app.models.user import User
from app.crud.user import create_user, get_user, get_user_by_email
from app.schemas.user import UserCreate, UserResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = create_user(db, user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> UserResponse:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# @router.get("/", response_model=List[UserResponse])
# def read_users(
#     db: Session = Depends(get_db)
# ) -> List[UserResponse]:
#     users = db.query(User).all()
#     if not users:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No users found"
#         )
#     return users    