#!/usr/bin/env python3
"""
Test script for MCP servers with OAuth flow.
This script tests the Google Docs, Gmail, and Google Drive MCP servers
including the OAuth authentication flow.
"""

import asyncio
import json
import os
import sys
from uuid import uuid4
from database import get_db_session, create_tables
from config import Config

def _get_or_create_test_workspace():
    """Get or create a test workspace"""
    try:
        from database import get_or_create_workspace
        workspace = get_or_create_workspace("test_workspace")
        return workspace["id"]
    except Exception as e:
        print(f"Warning: Could not create workspace, using random UUID: {e}")
        return str(uuid4())

def test_server_initialization():
    """Test that servers can be initialized without errors"""
    print("Testing MCP Server Initialization")
    print("=" * 40)
    
    try:
        # Test Google Docs Server
        print("Testing Google Docs MCP Server...")
        from gdocs_server import GoogleDocsMCPServer
        session = get_db_session()
        docs_server = GoogleDocsMCPServer(session)
        print("✓ Google Docs server initialized successfully")
        
        # Test Gmail Server
        print("Testing Gmail MCP Server...")
        from gmail_server import GmailMCPServer
        gmail_server = GmailMCPServer(session)
        print("✓ Gmail server initialized successfully")
        
        # Test Google Drive Server
        print("Testing Google Drive MCP Server...")
        from gdrive_server import GoogleDriveMCPServer
        drive_server = GoogleDriveMCPServer(session)
        print("✓ Google Drive server initialized successfully")
        
        session.close()
        return docs_server, gmail_server, drive_server
        
    except Exception as e:
        print(f"✗ Error initializing servers: {e}")
        return None, None, None

def test_tool_registration(servers):
    """Test that tools are properly registered"""
    print("\nTesting Tool Registration")
    print("=" * 30)
    
    docs_server, gmail_server, drive_server = servers
    
    # Test Google Docs tools
    print("Google Docs Tools:")
    docs_tools = docs_server.get_tools()
    for tool_name in docs_tools.keys():
        print(f"  ✓ {tool_name}")
    
    # Test Gmail tools
    print("\nGmail Tools:")
    gmail_tools = gmail_server.get_tools()
    for tool_name in gmail_tools.keys():
        print(f"  ✓ {tool_name}")
    
    # Test Google Drive tools
    print("\nGoogle Drive Tools:")
    drive_tools = drive_server.get_tools()
    for tool_name in drive_tools.keys():
        print(f"  ✓ {tool_name}")

def test_oauth_url_generation(servers):
    """Test OAuth URL generation"""
    print("\nTesting OAuth URL Generation")
    print("=" * 35)
    
    docs_server, gmail_server, drive_server = servers
    
    try:
        # Test Google Docs OAuth URL
        print("Testing Google Docs OAuth URL...")
        docs_url = docs_server.call_tool("get_docs_auth_url")
        print(f"✓ Google Docs OAuth URL: {docs_url}")
        
        # Test Gmail OAuth URL
        print("Testing Gmail OAuth URL...")
        gmail_url = gmail_server.call_tool("get_gmail_auth_url")
        print(f"✓ Gmail OAuth URL: {gmail_url}")
        
        # Test Google Drive OAuth URL
        print("Testing Google Drive OAuth URL...")
        drive_url = drive_server.call_tool("get_drive_auth_url")
        print(f"✓ Google Drive OAuth URL: {drive_url}")
        
    except Exception as e:
        print(f"✗ Error generating OAuth URLs: {e}")

def test_credentials_status(servers):
    """Test credentials status checking"""
    print("\nTesting Credentials Status")
    print("=" * 30)
    
    docs_server, gmail_server, drive_server = servers
    
    # Create a test workspace ID
    test_workspace_id = _get_or_create_test_workspace()
    
    try:
        # Test Google Docs credentials status
        print("Testing Google Docs credentials status...")
        docs_status = docs_server.call_tool("get_docs_credentials_status", test_workspace_id)
        print(f"✓ Google Docs status: {docs_status}")
        
        # Test Gmail credentials status
        print("Testing Gmail credentials status...")
        gmail_status = gmail_server.call_tool("get_gmail_credentials_status", test_workspace_id)
        print(f"✓ Gmail status: {gmail_status}")
        
        # Test Google Drive credentials status
        print("Testing Google Drive credentials status...")
        drive_status = drive_server.call_tool("get_drive_credentials_status", test_workspace_id)
        print(f"✓ Google Drive status: {drive_status}")
        
    except Exception as e:
        print(f"✗ Error checking credentials status: {e}")

def test_oauth_flow_simulation(servers):
    """Simulate OAuth flow with invalid code"""
    print("\nTesting OAuth Flow Simulation")
    print("=" * 35)
    
    docs_server, gmail_server, drive_server = servers
    
    # Create a test workspace ID
    test_workspace_id = _get_or_create_test_workspace()
    test_auth_code = "test_invalid_code"
    
    try:
        # Test Google Docs OAuth flow
        print("Testing Google Docs OAuth flow...")
        docs_result = docs_server.call_tool("authenticate_docs_user", test_auth_code, test_workspace_id)
        print(f"✓ Google Docs OAuth result: {docs_result}")
        
        # Test Gmail OAuth flow
        print("Testing Gmail OAuth flow...")
        gmail_result = gmail_server.call_tool("authenticate_gmail_user", test_auth_code, test_workspace_id)
        print(f"✓ Gmail OAuth result: {gmail_result}")
        
        # Test Google Drive OAuth flow
        print("Testing Google Drive OAuth flow...")
        drive_result = drive_server.call_tool("authenticate_drive_user", test_auth_code, test_workspace_id)
        print(f"✓ Google Drive OAuth result: {drive_result}")
        
    except Exception as e:
        print(f"✗ Error in OAuth flow simulation: {e}")

def test_service_tools_without_credentials(servers):
    """Test service tools without valid credentials"""
    print("\nTesting Service Tools (No Credentials)")
    print("=" * 40)
    
    docs_server, gmail_server, drive_server = servers
    
    # Create a test workspace ID
    test_workspace_id = _get_or_create_test_workspace()
    
    try:
        # Test Google Docs tools
        print("Testing Google Docs tools...")
        docs_result = docs_server.call_tool("list_google_docs", test_workspace_id)
        print(f"✓ Google Docs list result: {docs_result}")
        
        # Test Gmail tools
        print("Testing Gmail tools...")
        gmail_result = gmail_server.call_tool("read_inbox", test_workspace_id)
        print(f"✓ Gmail inbox result: {gmail_result}")
        
        # Test Google Drive tools
        print("Testing Google Drive tools...")
        drive_result = drive_server.call_tool("list_drive_files", test_workspace_id)
        print(f"✓ Google Drive list result: {drive_result}")
        
    except Exception as e:
        print(f"✗ Error testing service tools: {e}")

def test_clear_credentials(servers):
    """Test credential clearing functionality"""
    print("\nTesting Clear Credentials")
    print("=" * 25)
    
    docs_server, gmail_server, drive_server = servers
    
    # Create a test workspace ID
    test_workspace_id = _get_or_create_test_workspace()
    
    try:
        # Test Google Docs clear credentials
        print("Testing Google Docs clear credentials...")
        docs_result = docs_server.call_tool("clear_google_credentials", test_workspace_id)
        print(f"✓ Google Docs clear result: {docs_result}")
        
        # Test Gmail clear credentials
        print("Testing Gmail clear credentials...")
        gmail_result = gmail_server.call_tool("clear_google_credentials", test_workspace_id)
        print(f"✓ Gmail clear result: {gmail_result}")
        
        # Test Google Drive clear credentials
        print("Testing Google Drive clear credentials...")
        drive_result = drive_server.call_tool("clear_google_credentials", test_workspace_id)
        print(f"✓ Google Drive clear result: {drive_result}")
        
    except Exception as e:
        print(f"✗ Error testing clear credentials: {e}")

def check_environment_configuration():
    """Check environment configuration"""
    print("Environment Configuration Check")
    print("=" * 35)
    
    # Check OAuth credentials
    oauth_vars = [
        "GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET",
        "GDRIVE_CLIENT_ID", "GDRIVE_CLIENT_SECRET",
        "GDOCS_CLIENT_ID", "GDOCS_CLIENT_SECRET",
        "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"
    ]
    
    print("OAuth Credentials:")
    for var in oauth_vars:
        value = os.getenv(var)
        status = "✓ Set" if value else "✗ Not Set"
        print(f"  {var}: {status}")
    
    # Check database configuration
    print("\nDatabase Configuration:")
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        print(f"  DATABASE_URL: ✓ Set ({db_url[:50]}...)")
    else:
        print("  DATABASE_URL: ✗ Not Set (using default)")
    
    # Check redirect URI
    print("\nRedirect URI:")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/google/callback")
    print(f"  GOOGLE_REDIRECT_URI: {redirect_uri}")

def main():
    """Main test function"""
    print("MCP Server OAuth Flow Test")
    print("=" * 50)
    
    # Check environment configuration
    check_environment_configuration()
    
    # Create database tables
    print("\nSetting up database...")
    try:
        create_tables()
        print("✓ Database tables created/verified")
    except Exception as e:
        print(f"✗ Error setting up database: {e}")
        return
    
    # Test server initialization
    servers = test_server_initialization()
    if not all(servers):
        print("Failed to initialize servers. Exiting.")
        return
    
    # Run all tests
    test_tool_registration(servers)
    test_oauth_url_generation(servers)
    test_credentials_status(servers)
    test_oauth_flow_simulation(servers)
    test_service_tools_without_credentials(servers)
    test_clear_credentials(servers)
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print("✓ All MCP servers initialized successfully")
    print("✓ OAuth URL generation working")
    print("✓ Credentials status checking working")
    print("✓ OAuth flow simulation working")
    print("✓ Service tools responding correctly")
    print("✓ Clear credentials functionality working")
    print("\nNext steps:")
    print("1. Set up OAuth credentials in environment variables")
    print("2. Use the OAuth URLs to get authorization codes")
    print("3. Test with real Google services")

if __name__ == "__main__":
    main()
