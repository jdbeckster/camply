#!/usr/bin/env python3
"""
Simple test script to verify the backend works correctly
"""

import requests
import time
import sys

def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Camply Web Interface Backend...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working: {data.get('message', 'Unknown')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint failed: {e}")
        return False
    
    # Test search endpoints
    try:
        response = requests.get(f"{base_url}/api/search/providers", timeout=10)
        if response.status_code == 200:
            data = response.json()
            providers = data.get('providers', [])
            print(f"✅ Search providers endpoint working: {len(providers)} providers found")
        else:
            print(f"❌ Search providers endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Search providers endpoint failed: {e}")
        return False
    
    # Test recreation areas search
    try:
        response = requests.get(f"{base_url}/api/search/recreation-areas?query=Glacier", timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ Recreation areas search working: {len(results)} results found")
        else:
            print(f"❌ Recreation areas search failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Recreation areas search failed: {e}")
        return False
    
    print("🎉 All tests passed! Backend is working correctly.")
    return True

if __name__ == "__main__":
    # Wait a moment for the server to start
    print("⏳ Waiting for backend to start...")
    time.sleep(2)
    
    success = test_backend()
    sys.exit(0 if success else 1) 