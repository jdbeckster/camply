"""
Database models for Camply Web Interface
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    notification_preferences = relationship("NotificationPreference", back_populates="user")
    notification_history = relationship("NotificationHistory", back_populates="user")


class NotificationPreference(Base):
    """Notification preferences model"""
    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recreation_area_id = Column(Integer, nullable=True)
    recreation_area_name = Column(String(255), nullable=True)
    campground_id = Column(Integer, nullable=True)
    campground_name = Column(String(255), nullable=True)
    campsite_id = Column(Integer, nullable=True)
    campsite_name = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    phone_number = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="notification_preferences")
    notification_history = relationship("NotificationHistory", back_populates="preference")


class NotificationHistory(Base):
    """Notification history model"""
    __tablename__ = "notification_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    preference_id = Column(Integer, ForeignKey("notification_preferences.id"), nullable=True)
    campsite_id = Column(Integer, nullable=True)
    campsite_name = Column(String(255), nullable=True)
    notification_type = Column(String(50), nullable=False)  # 'sms', 'email', etc.
    message = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="notification_history")
    preference = relationship("NotificationPreference", back_populates="notification_history") 