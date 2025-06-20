"""
Authentication API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.models import User
from app.models.schemas import UserCreate, User
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=User)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    auth_service = AuthService(db)
    
    # Check if user already exists
    existing_user = auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user
    user = auth_service.create_user(user_data)
    return user


@router.get("/me", response_model=User)
async def get_current_user(
    db: Session = Depends(get_db)
):
    """Get current user information"""
    # For now, we'll use a simple approach - in production you'd use JWT tokens
    # This is a placeholder for the actual authentication logic
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication not yet implemented"
    ) 