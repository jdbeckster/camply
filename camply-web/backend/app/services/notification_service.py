"""
Notification service for managing preferences and sending notifications
"""

import sys
import os
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

# Add the parent camply directory to the path so we can import camply modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../'))

from app.models.models import NotificationPreference, NotificationHistory, User
from app.models.schemas import NotificationPreferenceCreate, NotificationPreferenceUpdate


class NotificationService:
    """Service for handling notification operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification_preference(
        self,
        user_id: int,
        notification_data: NotificationPreferenceCreate
    ) -> NotificationPreference:
        """Create a new notification preference"""
        # Verify user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Create notification preference
        notification = NotificationPreference(
            user_id=user_id,
            recreation_area_id=notification_data.recreation_area_id,
            recreation_area_name=notification_data.recreation_area_name,
            campground_id=notification_data.campground_id,
            campground_name=notification_data.campground_name,
            campsite_id=notification_data.campsite_id,
            campsite_name=notification_data.campsite_name,
            start_date=notification_data.start_date,
            end_date=notification_data.end_date,
            phone_number=notification_data.phone_number,
            is_active=True
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def get_notification_preferences(
        self,
        user_id: int,
        active_only: bool = True
    ) -> List[NotificationPreference]:
        """Get notification preferences for a user"""
        query = self.db.query(NotificationPreference).filter(
            NotificationPreference.user_id == user_id
        )
        
        if active_only:
            query = query.filter(NotificationPreference.is_active == True)
        
        return query.all()
    
    def get_notification_preference(self, notification_id: int) -> Optional[NotificationPreference]:
        """Get a specific notification preference"""
        return self.db.query(NotificationPreference).filter(
            NotificationPreference.id == notification_id
        ).first()
    
    def update_notification_preference(
        self,
        notification_id: int,
        notification_data: NotificationPreferenceUpdate
    ) -> Optional[NotificationPreference]:
        """Update a notification preference"""
        notification = self.get_notification_preference(notification_id)
        if not notification:
            return None
        
        # Update fields that are provided
        update_data = notification_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(notification, key, value)
        
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def delete_notification_preference(self, notification_id: int) -> bool:
        """Delete a notification preference"""
        notification = self.get_notification_preference(notification_id)
        if not notification:
            return False
        
        self.db.delete(notification)
        self.db.commit()
        
        return True
    
    def get_notification_history(
        self,
        notification_id: int,
        limit: int = 50
    ) -> List[NotificationHistory]:
        """Get notification history for a specific preference"""
        return self.db.query(NotificationHistory).filter(
            NotificationHistory.preference_id == notification_id
        ).order_by(NotificationHistory.sent_at.desc()).limit(limit).all()
    
    def send_test_notification(self, notification_id: int) -> bool:
        """Send a test notification"""
        notification = self.get_notification_preference(notification_id)
        if not notification:
            return False
        
        try:
            # Try to send via camply's notification system
            self._send_via_camply(notification, "Test notification from Camply Web Interface")
            
            # Record the notification
            history = NotificationHistory(
                user_id=notification.user_id,
                preference_id=notification.id,
                notification_type="sms",
                message="Test notification sent successfully",
                success=True
            )
            self.db.add(history)
            self.db.commit()
            
            return True
            
        except Exception as e:
            # Record the failure
            history = NotificationHistory(
                user_id=notification.user_id,
                preference_id=notification.id,
                notification_type="sms",
                message="Test notification failed",
                success=False,
                error_message=str(e)
            )
            self.db.add(history)
            self.db.commit()
            
            return False
    
    def _send_via_camply(
        self,
        notification: NotificationPreference,
        message: str
    ) -> None:
        """Send notification via camply's notification system"""
        try:
            # Import camply notification modules
            from camply.notifications import TwilioNotifications
            
            # Create notification instance
            notifier = TwilioNotifications()
            
            # Send the message
            notifier.send_message(message)
            
        except Exception as e:
            # If camply notification fails, we could implement a fallback
            # For now, just log the error
            print(f"Failed to send notification via camply: {e}")
            raise
    
    def start_background_search(self, notification_id: int) -> bool:
        """Start a background search for the notification preference"""
        notification = self.get_notification_preference(notification_id)
        if not notification:
            return False
        
        try:
            # This would typically use Celery or similar task queue
            # For now, we'll just log that we would start a search
            print(f"Would start background search for notification {notification_id}")
            
            # In a real implementation, you would:
            # 1. Create a Celery task
            # 2. Pass the notification preference to the task
            # 3. The task would use camply to search for campsites
            # 4. When found, it would send notifications
            
            return True
            
        except Exception as e:
            print(f"Failed to start background search: {e}")
            return False
    
    def stop_background_search(self, notification_id: int) -> bool:
        """Stop a background search for the notification preference"""
        try:
            # This would typically cancel a Celery task
            # For now, we'll just log that we would stop a search
            print(f"Would stop background search for notification {notification_id}")
            
            return True
            
        except Exception as e:
            print(f"Failed to stop background search: {e}")
            return False 