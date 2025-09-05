#!/usr/bin/env python3
"""
Quick test script to verify web interface components
"""

def test_imports():
    """Test all imports"""
    print("🧪 Testing imports...")
    
    try:
        from models.workspace import Workspace, Integration, WorkspaceIntegrationLink
        print("✅ Models imported successfully")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from database import create_tables, get_db_session, create_workspace
        print("✅ Database functions imported successfully")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        from auth.oauth import GoogleOAuth
        print("✅ OAuth class imported successfully")
    except Exception as e:
        print(f"❌ OAuth import failed: {e}")
        return False
    
    try:
        from web_interface import app
        print("✅ Web interface imported successfully")
    except Exception as e:
        print(f"❌ Web interface import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database operations"""
    print("\n🧪 Testing database operations...")
    
    try:
        from database import create_tables, create_workspace, get_workspace_by_name
        
        # Create tables
        create_tables()
        print("✅ Tables created successfully")
        
        # Test workspace creation
        test_username = "quick_test_user"
        workspace = create_workspace(test_username)
        print(f"✅ Workspace created: {workspace}")
        
        # Test retrieval
        retrieved = get_workspace_by_name(test_username)
        print(f"✅ Workspace retrieved: {retrieved}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_oauth():
    """Test OAuth class"""
    print("\n🧪 Testing OAuth class...")
    
    try:
        from auth.oauth import GoogleOAuth
        from database import get_db_session
        
        session = get_db_session()
        oauth = GoogleOAuth(session, "gmail")
        print("✅ OAuth instance created successfully")
        
        # Test authorization URL generation (will fail without env vars, but that's expected)
        try:
            auth_url = oauth.get_authorization_url()
            print("✅ Authorization URL generated successfully")
        except ValueError as e:
            print(f"⚠️  Authorization URL failed (expected without env vars): {e}")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ OAuth test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting quick tests...\n")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test database
    database_ok = test_database()
    
    # Test OAuth
    oauth_ok = test_oauth()
    
    # Summary
    print(f"\n📋 Test Summary:")
    print(f"   Imports: {'✅ OK' if imports_ok else '❌ Failed'}")
    print(f"   Database: {'✅ OK' if database_ok else '❌ Failed'}")
    print(f"   OAuth: {'✅ OK' if oauth_ok else '❌ Failed'}")
    
    if all([imports_ok, database_ok, oauth_ok]):
        print(f"\n🎉 All tests passed! The web interface should work correctly.")
        print(f"   Next: Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables")
        print(f"   Then run: python web_interface.py")
    else:
        print(f"\n😞 Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
