import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { useNavigate } from 'react-router-dom';
import { createNotification } from '../api/notifications';
import { searchRecreationAreas, searchCampgrounds, searchCampsites } from '../api/search';

interface SearchResult {
  id: number;
  name: string;
  description?: string;
  location?: string;
}

const NotificationForm: React.FC = () => {
  const navigate = useNavigate();
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Search states
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);
  const [searchType, setSearchType] = useState<'recreation-area' | 'campground' | 'campsite'>('recreation-area');

  // Selected items
  const [selectedRecreationArea, setSelectedRecreationArea] = useState<SearchResult | null>(null);
  const [selectedCampground, setSelectedCampground] = useState<SearchResult | null>(null);
  const [selectedCampsite, setSelectedCampsite] = useState<SearchResult | null>(null);

  const handleSearch = async (query: string) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    setSearching(true);
    try {
      let results: SearchResult[] = [];
      
      switch (searchType) {
        case 'recreation-area':
          const recAreas = await searchRecreationAreas(query);
          results = recAreas.results;
          break;
        case 'campground':
          const campgrounds = await searchCampgrounds(query);
          results = campgrounds.results;
          break;
        case 'campsite':
          const campsites = await searchCampsites(query);
          results = campsites.results;
          break;
      }
      
      setSearchResults(results);
    } catch (err) {
      setError('Failed to search. Please try again.');
    } finally {
      setSearching(false);
    }
  };

  const handleSearchTypeChange = (type: 'recreation-area' | 'campground' | 'campsite') => {
    setSearchType(type);
    setSearchQuery('');
    setSearchResults([]);
    setSelectedRecreationArea(null);
    setSelectedCampground(null);
    setSelectedCampsite(null);
  };

  const handleResultSelect = (result: SearchResult) => {
    switch (searchType) {
      case 'recreation-area':
        setSelectedRecreationArea(result);
        setSearchType('campground');
        break;
      case 'campground':
        setSelectedCampground(result);
        setSearchType('campsite');
        break;
      case 'campsite':
        setSelectedCampsite(result);
        break;
    }
    setSearchQuery('');
    setSearchResults([]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!startDate || !endDate || !phoneNumber) {
      setError('Please fill in all required fields.');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const notificationData = {
        recreation_area_id: selectedRecreationArea?.id,
        recreation_area_name: selectedRecreationArea?.name,
        campground_id: selectedCampground?.id,
        campground_name: selectedCampground?.name,
        campsite_id: selectedCampsite?.id,
        campsite_name: selectedCampsite?.name,
        start_date: startDate.toISOString().split('T')[0],
        end_date: endDate.toISOString().split('T')[0],
        phone_number: phoneNumber
      };

      await createNotification(notificationData);
      setSuccess('Notification created successfully! You will receive SMS alerts when campsites become available.');
      
      // Redirect to notifications list after a short delay
      setTimeout(() => {
        navigate('/notifications');
      }, 2000);

    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create notification. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h1 className="card-title">Create Campsite Alert</h1>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        <form onSubmit={handleSubmit}>
          {/* Date Range Selection */}
          <div className="form-group">
            <label>Date Range *</label>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <DatePicker
                selected={startDate}
                onChange={(date) => setStartDate(date)}
                selectsStart
                startDate={startDate}
                endDate={endDate}
                minDate={new Date()}
                placeholderText="Start Date"
                className="form-control"
                dateFormat="MM/dd/yyyy"
              />
              <span>to</span>
              <DatePicker
                selected={endDate}
                onChange={(date) => setEndDate(date)}
                selectsEnd
                startDate={startDate}
                endDate={endDate}
                minDate={startDate || new Date()}
                placeholderText="End Date"
                className="form-control"
                dateFormat="MM/dd/yyyy"
              />
            </div>
          </div>

          {/* Location Selection */}
          <div className="form-group">
            <label>Location Selection</label>
            
            {/* Search Type Selector */}
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ marginRight: '1rem' }}>
                <input
                  type="radio"
                  name="searchType"
                  checked={searchType === 'recreation-area'}
                  onChange={() => handleSearchTypeChange('recreation-area')}
                />
                Recreation Area
              </label>
              <label style={{ marginRight: '1rem' }}>
                <input
                  type="radio"
                  name="searchType"
                  checked={searchType === 'campground'}
                  onChange={() => handleSearchTypeChange('campground')}
                />
                Campground
              </label>
              <label>
                <input
                  type="radio"
                  name="searchType"
                  checked={searchType === 'campsite'}
                  onChange={() => handleSearchTypeChange('campsite')}
                />
                Campsite
              </label>
            </div>

            {/* Search Input */}
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                handleSearch(e.target.value);
              }}
              placeholder={`Search for ${searchType.replace('-', ' ')}...`}
              className="form-control"
            />

            {/* Search Results */}
            {searchResults.length > 0 && (
              <div className="search-results">
                {searchResults.map((result) => (
                  <div
                    key={result.id}
                    className="search-result-item"
                    onClick={() => handleResultSelect(result)}
                  >
                    <div className="search-result-name">{result.name}</div>
                    {result.description && (
                      <div className="search-result-description">{result.description}</div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Selected Items Display */}
            {selectedRecreationArea && (
              <div style={{ marginTop: '1rem', padding: '0.5rem', background: '#e9ecef', borderRadius: '5px' }}>
                <strong>Selected Recreation Area:</strong> {selectedRecreationArea.name}
              </div>
            )}
            {selectedCampground && (
              <div style={{ marginTop: '0.5rem', padding: '0.5rem', background: '#e9ecef', borderRadius: '5px' }}>
                <strong>Selected Campground:</strong> {selectedCampground.name}
              </div>
            )}
            {selectedCampsite && (
              <div style={{ marginTop: '0.5rem', padding: '0.5rem', background: '#e9ecef', borderRadius: '5px' }}>
                <strong>Selected Campsite:</strong> {selectedCampsite.name}
              </div>
            )}
          </div>

          {/* Phone Number */}
          <div className="form-group">
            <label>Phone Number (for SMS alerts) *</label>
            <input
              type="tel"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="+1 (555) 123-4567"
              className="form-control"
              required
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ marginTop: '1rem' }}
          >
            {loading ? 'Creating Alert...' : 'Create Alert'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default NotificationForm; 