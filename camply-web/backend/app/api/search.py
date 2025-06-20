"""
Search API endpoints for recreation areas, campgrounds, and campsites
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import (
    SearchResponse, 
    RecreationAreaSearch, 
    CampgroundSearch, 
    CampsiteSearch
)
from app.services.search_service import SearchService

router = APIRouter()


@router.get("/recreation-areas", response_model=SearchResponse)
async def search_recreation_areas(
    query: Optional[str] = Query(None, description="Search term for recreation areas"),
    state: Optional[str] = Query(None, description="State code filter"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db)
):
    """Search for recreation areas"""
    search_service = SearchService(db)
    
    try:
        results = search_service.search_recreation_areas(
            query=query,
            state=state,
            page=page,
            per_page=per_page
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching recreation areas: {str(e)}"
        )


@router.get("/campgrounds", response_model=SearchResponse)
async def search_campgrounds(
    recreation_area_id: Optional[int] = Query(None, description="Recreation area ID"),
    query: Optional[str] = Query(None, description="Search term for campgrounds"),
    state: Optional[str] = Query(None, description="State code filter"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db)
):
    """Search for campgrounds"""
    search_service = SearchService(db)
    
    try:
        results = search_service.search_campgrounds(
            recreation_area_id=recreation_area_id,
            query=query,
            state=state,
            page=page,
            per_page=per_page
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching campgrounds: {str(e)}"
        )


@router.get("/campsites", response_model=SearchResponse)
async def search_campsites(
    campground_id: Optional[int] = Query(None, description="Campground ID"),
    recreation_area_id: Optional[int] = Query(None, description="Recreation area ID"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db)
):
    """Search for campsites"""
    search_service = SearchService(db)
    
    try:
        results = search_service.search_campsites(
            campground_id=campground_id,
            recreation_area_id=recreation_area_id,
            page=page,
            per_page=per_page
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching campsites: {str(e)}"
        )


@router.get("/providers")
async def get_providers():
    """Get list of available camping providers"""
    # This will return the list of providers that camply supports
    providers = [
        {
            "name": "RecreationDotGov",
            "description": "Recreation.gov - US National Parks and Federal Lands",
            "supported_features": ["campsites", "tickets", "timed_entries"]
        },
        {
            "name": "Yellowstone",
            "description": "Yellowstone National Park Lodges",
            "supported_features": ["campsites"]
        },
        {
            "name": "ReserveCalifornia",
            "description": "California State Parks",
            "supported_features": ["campsites"]
        },
        {
            "name": "GoingToCamp",
            "description": "Multiple Canadian and US State Parks",
            "supported_features": ["campsites"]
        }
    ]
    return {"providers": providers} 