"""
Pydantic schemas for API requests and responses
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user"""
    pass


class User(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationPreferenceBase(BaseModel):
    """Base notification preference schema"""
    recreation_area_id: Optional[int] = None
    recreation_area_name: Optional[str] = None
    campground_id: Optional[int] = None
    campground_name: Optional[str] = None
    campsite_id: Optional[int] = None
    campsite_name: Optional[str] = None
    start_date: date
    end_date: date
    phone_number: str

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class NotificationPreferenceCreate(NotificationPreferenceBase):
    """Schema for creating notification preference"""
    pass


class NotificationPreferenceUpdate(BaseModel):
    """Schema for updating notification preference"""
    recreation_area_id: Optional[int] = None
    recreation_area_name: Optional[str] = None
    campground_id: Optional[int] = None
    campground_name: Optional[str] = None
    campsite_id: Optional[int] = None
    campsite_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None


class NotificationPreference(NotificationPreferenceBase):
    """Schema for notification preference response"""
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationHistoryBase(BaseModel):
    """Base notification history schema"""
    campsite_id: Optional[int] = None
    campsite_name: Optional[str] = None
    notification_type: str
    message: str
    success: bool = True
    error_message: Optional[str] = None


class NotificationHistory(NotificationHistoryBase):
    """Schema for notification history response"""
    id: int
    user_id: int
    preference_id: Optional[int] = None
    sent_at: datetime

    class Config:
        from_attributes = True


class SearchResult(BaseModel):
    """Schema for search results"""
    id: int
    name: str
    description: Optional[str] = None
    location: Optional[str] = None


class RecreationAreaSearch(SearchResult):
    """Schema for recreation area search results"""
    pass


class CampgroundSearch(SearchResult):
    """Schema for campground search results"""
    recreation_area_id: int
    recreation_area_name: str


class CampsiteSearch(SearchResult):
    """Schema for campsite search results"""
    campground_id: int
    campground_name: str
    campsite_type: Optional[str] = None
    max_occupancy: Optional[int] = None


class SearchResponse(BaseModel):
    """Schema for search response"""
    results: List[SearchResult]
    total: int
    page: int
    per_page: int


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    error_code: Optional[str] = None 