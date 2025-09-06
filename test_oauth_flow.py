#!/usr/bin/env python3
"""
Simple OAuth flow test script.
This script helps you test the OAuth flow with proper workspace setup.
"""

import os
import sys
from database import get_db_session, create_tables, get_or_create_workspace
from config import Config

def test_oauth_flow():
    """Test OAuth flow with proper workspace setup"""
    print("OAuth Flow Test")
    print("=" * 20)
    
    # Check environment
    print("Checking environment...")
    if not os.getenv("GOOGLE_CLIENT_ID") or not os.getenv("GOOGLE_CLIENT_SECRET"):
        print("✗ Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET")
        print("Please set these environment variables first.")
        return
    
    print("✓ Environment variables set")
    
    # Create database tables
    print("Setting up database...")
    try:
        create_tables()
        print("✓ Database tables created/verified")
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        return
    
    # Create test workspace
    print("Creating test workspace...")
    try:
        workspace = get_or_create_workspace("test_workspace")
        workspace_id = workspace["id"]
        print(f"✓ Test workspace created: {workspace_id}")
    except Exception as e:
        print(f"✗ Workspace creation failed: {e}")
        return
    
    # Test OAuth URL generation
    print("\nTesting OAuth URL generation...")
    try:
        from gdocs_server import GoogleDocsMCPServer
        from gmail_server import GmailMCPServer
        from gdrive_server import GoogleDriveMCPServer
        
        session = get_db_session()
        
        # Test Google Docs
        docs_server = GoogleDocsMCPServer(session)
        docs_url = docs_server.call_tool("get_docs_auth_url")
        print(f"✓ Google Docs OAuth URL: {docs_url}")
        
        # Test Gmail
        gmail_server = GmailMCPServer(session)
        gmail_url = gmail_server.call_tool("get_gmail_auth_url")
        print(f"✓ Gmail OAuth URL: {gmail_url}")
        
        # Test Google Drive
        drive_server = GoogleDriveMCPServer(session)
        drive_url = drive_server.call_tool("get_drive_auth_url")
        print(f"✓ Google Drive OAuth URL: {drive_url}")
        
        session.close()
        
    except Exception as e:
        print(f"✗ OAuth URL generation failed: {e}")
        return
    
    print("\n" + "=" * 50)
    print("OAuth Flow Test Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Copy one of the OAuth URLs above")
    print("2. Open it in your browser")
    print("3. Sign in to Google and grant permissions")
    print("4. Copy the authorization code from the callback URL")
    print("5. Use the authorization code to test the OAuth flow")
    print("\nExample:")
    print("python test_web_oauth.py")
    print("Choose option 2, enter service and authorization code")

if __name__ == "__main__":
    test_oauth_flow()
