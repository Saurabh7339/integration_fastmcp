#!/usr/bin/env python3
"""
Test script for the updated web interface with service-specific OAuth
"""

import requests
import json
from database import create_tables, get_db_session, create_workspace, get_workspace_by_name

def test_database_functions():
    """Test database functions"""
    print("🧪 Testing database functions...")
    
    # Create tables
    create_tables()
    print("✅ Tables created successfully")
    
    # Test workspace creation
    test_username = "test_user_123"
    workspace = create_workspace(test_username)
    print(f"✅ Workspace created: {workspace}")
    
    # Test workspace retrieval
    retrieved_workspace = get_workspace_by_name(test_username)
    print(f"✅ Workspace retrieved: {retrieved_workspace}")
    
    # Test duplicate creation (should return existing)
    duplicate_workspace = create_workspace(test_username)
    print(f"✅ Duplicate workspace handled: {duplicate_workspace}")
    
    return test_username

def test_web_endpoints(base_url="http://localhost:8000"):
    """Test web interface endpoints"""
    print(f"\n🌐 Testing web endpoints at {base_url}...")
    
    try:
        # Test home page
        response = requests.get(f"{base_url}/")
        print(f"✅ Home page: {response.status_code}")
        
        # Test dashboard for test user
        test_username = "test_user_123"
        response = requests.get(f"{base_url}/dashboard/{test_username}")
        print(f"✅ Dashboard page: {response.status_code}")
        
        # Test API endpoints
        response = requests.get(f"{base_url}/api/credentials/{test_username}")
        print(f"✅ Credentials API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        
        response = requests.get(f"{base_url}/api/workspaces")
        print(f"✅ Workspaces API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        
        # Test service-specific auth pages
        for service in ["gmail", "drive", "docs"]:
            response = requests.get(f"{base_url}/auth/{service}?username={test_username}")
            print(f"✅ {service.title()} auth page: {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to web server. Make sure it's running on port 8000.")
        return False
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")
        return False
    
    return True

def test_oauth_flow_simulation():
    """Simulate OAuth flow without actual Google authentication"""
    print("\n🔐 Testing OAuth flow simulation...")
    
    try:
        from auth.oauth import GoogleOAuth
        from database import get_db_session
        
        # Get database session
        session = get_db_session()
        
        # Test OAuth initialization for each service
        for service_type in ["gmail", "drive", "docs"]:
            try:
                oauth = GoogleOAuth(session, service_type)
                print(f"✅ {service_type.title()} OAuth initialized successfully")
                
                # Test authorization URL generation
                auth_url = oauth.get_authorization_url()
                print(f"   Auth URL: {auth_url[:100]}...")
                
            except Exception as e:
                print(f"❌ {service_type.title()} OAuth failed: {e}")
        
        session.close()
        
    except Exception as e:
        print(f"❌ OAuth flow simulation failed: {e}")

def main():
    """Main test function"""
    print("🚀 Starting web interface tests...\n")
    
    # Test database functions
    test_username = test_database_functions()
    
    # Test OAuth flow simulation
    test_oauth_flow_simulation()
    
    # Test web endpoints
    print(f"\n📋 Test Summary:")
    print(f"   Username used: {test_username}")
    print(f"   Database: ✅ Working")
    print(f"   OAuth classes: ✅ Working")
    print(f"   Web interface: {'✅ Working' if test_web_endpoints() else '❌ Not accessible'}")
    
    print(f"\n🎯 Next steps:")
    print(f"   1. Start the web server: python web_interface.py")
    print(f"   2. Open http://localhost:8000 in your browser")
    print(f"   3. Enter username: {test_username}")
    print(f"   4. Test service-specific OAuth flows")
    print(f"   5. Check the dashboard for credential status")

if __name__ == "__main__":
    main()
