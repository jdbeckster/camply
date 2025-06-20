"""
Search service that integrates with camply's search functionality
"""

import sys
import os
from typing import List, Optional
from sqlalchemy.orm import Session

# Add the parent camply directory to the path so we can import camply modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../'))

from app.models.schemas import SearchResponse, SearchResult


class SearchService:
    """Service for handling search operations using camply"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def search_recreation_areas(
        self,
        query: Optional[str] = None,
        state: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> SearchResponse:
        """Search for recreation areas using camply"""
        try:
            # Import camply modules
            from camply.providers import RecreationDotGov
            
            # Create provider instance
            provider = RecreationDotGov()
            
            # Search for recreation areas
            if query:
                results = provider.find_recreation_areas(query=query, state=state)
            else:
                # If no query, return some popular areas
                results = provider.find_recreation_areas(query="National Park")
            
            # Convert to our schema format
            search_results = []
            for result in results:
                search_results.append(SearchResult(
                    id=result.recreation_area_id,
                    name=result.recreation_area,
                    description=result.recreation_area_location,
                    location=result.recreation_area_location
                ))
            
            # Apply pagination
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            paginated_results = search_results[start_idx:end_idx]
            
            return SearchResponse(
                results=paginated_results,
                total=len(search_results),
                page=page,
                per_page=per_page
            )
            
        except Exception as e:
            # Fallback to mock data if camply is not available
            return self._get_mock_recreation_areas(query, page, per_page)
    
    def search_campgrounds(
        self,
        recreation_area_id: Optional[int] = None,
        query: Optional[str] = None,
        state: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> SearchResponse:
        """Search for campgrounds using camply"""
        try:
            # Import camply modules
            from camply.providers import RecreationDotGov
            
            # Create provider instance
            provider = RecreationDotGov()
            
            # Search for campgrounds
            if recreation_area_id:
                results = provider.find_campgrounds(recreation_area_id=recreation_area_id)
            elif query:
                results = provider.find_campgrounds(query=query, state=state)
            else:
                # Return some popular campgrounds
                results = provider.find_campgrounds(query="Campground")
            
            # Convert to our schema format
            search_results = []
            for result in results:
                search_results.append(SearchResult(
                    id=result.facility_id,
                    name=result.facility_name,
                    description=f"Campground in {result.recreation_area}",
                    location=result.recreation_area
                ))
            
            # Apply pagination
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            paginated_results = search_results[start_idx:end_idx]
            
            return SearchResponse(
                results=paginated_results,
                total=len(search_results),
                page=page,
                per_page=per_page
            )
            
        except Exception as e:
            # Fallback to mock data if camply is not available
            return self._get_mock_campgrounds(recreation_area_id, page, per_page)
    
    def search_campsites(
        self,
        campground_id: Optional[int] = None,
        recreation_area_id: Optional[int] = None,
        page: int = 1,
        per_page: int = 20
    ) -> SearchResponse:
        """Search for campsites using camply"""
        try:
            # Import camply modules
            from camply.providers import RecreationDotGov
            
            # Create provider instance
            provider = RecreationDotGov()
            
            # Search for campsites
            if campground_id:
                results = provider.find_campsites(campground_id=campground_id)
            elif recreation_area_id:
                # Get campgrounds first, then campsites
                campgrounds = provider.find_campgrounds(recreation_area_id=recreation_area_id)
                results = []
                for campground in campgrounds[:5]:  # Limit to first 5 campgrounds
                    campsites = provider.find_campsites(campground_id=campground.facility_id)
                    results.extend(campsites)
            else:
                results = []
            
            # Convert to our schema format
            search_results = []
            for result in results:
                search_results.append(SearchResult(
                    id=result.campsite_id,
                    name=result.campsite_site_name,
                    description=f"Campsite in {result.facility_name}",
                    location=result.facility_name
                ))
            
            # Apply pagination
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            paginated_results = search_results[start_idx:end_idx]
            
            return SearchResponse(
                results=paginated_results,
                total=len(search_results),
                page=page,
                per_page=per_page
            )
            
        except Exception as e:
            # Fallback to mock data if camply is not available
            return self._get_mock_campsites(campground_id, page, per_page)
    
    def _get_mock_recreation_areas(
        self,
        query: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> SearchResponse:
        """Return mock recreation areas for testing"""
        mock_areas = [
            SearchResult(id=2725, name="Glacier National Park", description="Montana", location="MT"),
            SearchResult(id=2907, name="Rocky Mountain National Park", description="Colorado", location="CO"),
            SearchResult(id=2582, name="Yosemite National Park", description="California", location="CA"),
            SearchResult(id=2843, name="Yellowstone National Park", description="Wyoming", location="WY"),
            SearchResult(id=2844, name="Grand Canyon National Park", description="Arizona", location="AZ"),
        ]
        
        # Filter by query if provided
        if query:
            mock_areas = [area for area in mock_areas if query.lower() in area.name.lower()]
        
        # Apply pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = mock_areas[start_idx:end_idx]
        
        return SearchResponse(
            results=paginated_results,
            total=len(mock_areas),
            page=page,
            per_page=per_page
        )
    
    def _get_mock_campgrounds(
        self,
        recreation_area_id: Optional[int] = None,
        page: int = 1,
        per_page: int = 20
    ) -> SearchResponse:
        """Return mock campgrounds for testing"""
        mock_campgrounds = [
            SearchResult(id=1001, name="Many Glacier Campground", description="Glacier National Park", location="Glacier National Park"),
            SearchResult(id=1002, name="Moraine Park Campground", description="Rocky Mountain National Park", location="Rocky Mountain National Park"),
            SearchResult(id=1003, name="Yosemite Valley Campground", description="Yosemite National Park", location="Yosemite National Park"),
            SearchResult(id=1004, name="Mammoth Campground", description="Yellowstone National Park", location="Yellowstone National Park"),
            SearchResult(id=1005, name="Mather Campground", description="Grand Canyon National Park", location="Grand Canyon National Park"),
        ]
        
        # Apply pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = mock_campgrounds[start_idx:end_idx]
        
        return SearchResponse(
            results=paginated_results,
            total=len(mock_campgrounds),
            page=page,
            per_page=per_page
        )
    
    def _get_mock_campsites(
        self,
        campground_id: Optional[int] = None,
        page: int = 1,
        per_page: int = 20
    ) -> SearchResponse:
        """Return mock campsites for testing"""
        mock_campsites = [
            SearchResult(id=2001, name="Site A01", description="Many Glacier Campground", location="Many Glacier Campground"),
            SearchResult(id=2002, name="Site A02", description="Many Glacier Campground", location="Many Glacier Campground"),
            SearchResult(id=2003, name="Site B01", description="Moraine Park Campground", location="Moraine Park Campground"),
            SearchResult(id=2004, name="Site B02", description="Moraine Park Campground", location="Moraine Park Campground"),
            SearchResult(id=2005, name="Site C01", description="Yosemite Valley Campground", location="Yosemite Valley Campground"),
        ]
        
        # Apply pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = mock_campsites[start_idx:end_idx]
        
        return SearchResponse(
            results=paginated_results,
            total=len(mock_campsites),
            page=page,
            per_page=per_page
        ) 