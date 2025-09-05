#!/usr/bin/env python3
"""
Test script for the main.py API endpoints
Demonstrates the complete OAuth flow
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all the API endpoints"""
    
    print("🧪 Testing Google Services MCP OAuth Integration API")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1️⃣ Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Create workspace
    print("\n2️⃣ Testing workspace creation...")
    try:
        username = "test_user_api"
        response = requests.post(f"{BASE_URL}/api/workspace", json={"name": username})
        if response.status_code == 200:
            workspace_data = response.json()
            print("✅ Workspace created successfully")
            print(f"   Workspace ID: {workspace_data['id']}")
            print(f"   Username: {workspace_data['name']}")
        else:
            print(f"❌ Workspace creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Workspace creation error: {e}")
    
    # Test 3: Get workspace
    print("\n3️⃣ Testing workspace retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/api/workspace/{username}")
        if response.status_code == 200:
            workspace_data = response.json()
            print("✅ Workspace retrieved successfully")
            print(f"   Workspace ID: {workspace_data['id']}")
            print(f"   Status: {workspace_data['status']}")
        else:
            print(f"❌ Workspace retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Workspace retrieval error: {e}")
    
    # Test 4: OAuth status check
    print("\n4️⃣ Testing OAuth status check...")
    try:
        response = requests.get(f"{BASE_URL}/api/oauth/status/{username}")
        if response.status_code == 200:
            status_data = response.json()
            print("✅ OAuth status retrieved successfully")
            print(f"   Workspace ID: {status_data['workspace_id']}")
            print("   Services status:")
            for service, status in status_data['services_status'].items():
                print(f"     {service}: {'✅ Authenticated' if status.get('is_authenticated') else '❌ Not authenticated'}")
        else:
            print(f"❌ OAuth status check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ OAuth status check error: {e}")
    
    # Test 5: OAuth initiation
    print("\n5️⃣ Testing OAuth initiation...")
    try:
        service = "gmail"
        response = requests.post(f"{BASE_URL}/api/oauth/initiate", json={
            "username": username,
            "service": service
        })
        if response.status_code == 200:
            oauth_data = response.json()
            print("✅ OAuth flow initiated successfully")
            print(f"   Service: {oauth_data['service']}")
            print(f"   Authorization URL: {oauth_data['authorization_url']}")
            print(f"   State: {oauth_data['state']}")
            print("\n   📝 Next steps:")
            print("   1. Open the authorization URL in a browser")
            print("   2. Complete Google OAuth consent")
            print("   3. You'll be redirected to the callback URL")
            print("   4. Use the returned code to complete authentication")
        else:
            print(f"❌ OAuth initiation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ OAuth initiation error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 API Testing Complete!")
    print("\n📚 To test the complete OAuth flow:")
    print("   1. Start the main.py server: python3 main.py")
    print("   2. Run this test script: python3 test_api.py")
    print("   3. Follow the OAuth flow in your browser")
    print("   4. Test the service functionality after authentication")

if __name__ == "__main__":
    test_api_endpoints()
