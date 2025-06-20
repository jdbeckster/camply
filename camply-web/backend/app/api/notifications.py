"""
Notifications API endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import (
    NotificationPreference,
    NotificationPreferenceCreate,
    NotificationPreferenceUpdate,
    NotificationHistory
)
from app.services.notification_service import NotificationService

router = APIRouter()


@router.post("/", response_model=NotificationPreference)
async def create_notification(
    notification_data: NotificationPreferenceCreate,
    db: Session = Depends(get_db)
):
    """Create a new notification preference"""
    notification_service = NotificationService(db)
    
    try:
        # For now, we'll use a default user ID (1) - in production this would come from auth
        user_id = 1
        notification = notification_service.create_notification_preference(
            user_id=user_id,
            notification_data=notification_data
        )
        return notification
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating notification: {str(e)}"
        )


@router.get("/", response_model=List[NotificationPreference])
async def get_notifications(
    user_id: Optional[int] = Query(None, description="User ID"),
    active_only: bool = Query(True, description="Return only active notifications"),
    db: Session = Depends(get_db)
):
    """Get notification preferences for a user"""
    notification_service = NotificationService(db)
    
    # For now, use default user ID
    if user_id is None:
        user_id = 1
    
    try:
        notifications = notification_service.get_notification_preferences(
            user_id=user_id,
            active_only=active_only
        )
        return notifications
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving notifications: {str(e)}"
        )


@router.get("/{notification_id}", response_model=NotificationPreference)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific notification preference"""
    notification_service = NotificationService(db)
    
    try:
        notification = notification_service.get_notification_preference(notification_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return notification
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving notification: {str(e)}"
        )


@router.put("/{notification_id}", response_model=NotificationPreference)
async def update_notification(
    notification_id: int,
    notification_data: NotificationPreferenceUpdate,
    db: Session = Depends(get_db)
):
    """Update a notification preference"""
    notification_service = NotificationService(db)
    
    try:
        notification = notification_service.update_notification_preference(
            notification_id=notification_id,
            notification_data=notification_data
        )
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return notification
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating notification: {str(e)}"
        )


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Delete a notification preference"""
    notification_service = NotificationService(db)
    
    try:
        success = notification_service.delete_notification_preference(notification_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return {"message": "Notification deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting notification: {str(e)}"
        )


@router.get("/{notification_id}/history", response_model=List[NotificationHistory])
async def get_notification_history(
    notification_id: int,
    limit: int = Query(50, ge=1, le=100, description="Number of history records to return"),
    db: Session = Depends(get_db)
):
    """Get notification history for a specific preference"""
    notification_service = NotificationService(db)
    
    try:
        history = notification_service.get_notification_history(
            notification_id=notification_id,
            limit=limit
        )
        return history
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving notification history: {str(e)}"
        )


@router.post("/{notification_id}/test")
async def test_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Send a test notification"""
    notification_service = NotificationService(db)
    
    try:
        success = notification_service.send_test_notification(notification_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return {"message": "Test notification sent successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending test notification: {str(e)}"
        ) 