import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface SearchResult {
  id: number;
  name: string;
  description?: string;
  location?: string;
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
  page: number;
  per_page: number;
}

export const searchRecreationAreas = async (
  query?: string,
  state?: string,
  page: number = 1,
  per_page: number = 20
): Promise<SearchResponse> => {
  const params = new URLSearchParams();
  if (query) params.append('query', query);
  if (state) params.append('state', state);
  params.append('page', page.toString());
  params.append('per_page', per_page.toString());
  
  const response = await axios.get(`${API_BASE_URL}/api/search/recreation-areas?${params}`);
  return response.data;
};

export const searchCampgrounds = async (
  recreation_area_id?: number,
  query?: string,
  state?: string,
  page: number = 1,
  per_page: number = 20
): Promise<SearchResponse> => {
  const params = new URLSearchParams();
  if (recreation_area_id) params.append('recreation_area_id', recreation_area_id.toString());
  if (query) params.append('query', query);
  if (state) params.append('state', state);
  params.append('page', page.toString());
  params.append('per_page', per_page.toString());
  
  const response = await axios.get(`${API_BASE_URL}/api/search/campgrounds?${params}`);
  return response.data;
};

export const searchCampsites = async (
  campground_id?: number,
  recreation_area_id?: number,
  page: number = 1,
  per_page: number = 20
): Promise<SearchResponse> => {
  const params = new URLSearchParams();
  if (campground_id) params.append('campground_id', campground_id.toString());
  if (recreation_area_id) params.append('recreation_area_id', recreation_area_id.toString());
  params.append('page', page.toString());
  params.append('per_page', per_page.toString());
  
  const response = await axios.get(`${API_BASE_URL}/api/search/campsites?${params}`);
  return response.data;
};

export const getProviders = async (): Promise<any[]> => {
  const response = await axios.get(`${API_BASE_URL}/api/search/providers`);
  return response.data.providers;
}; 