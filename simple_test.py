#!/usr/bin/env python3
"""
Simple test script that doesn't require external dependencies.
This tests the basic structure and imports of the MCP servers.
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing Module Imports")
    print("=" * 25)
    
    try:
        # Test FastMCP import
        print("Testing FastMCP import...")
        from fastmcp import FastMCP
        print("✓ FastMCP imported successfully")
        
        # Test config import
        print("Testing config import...")
        from config import Config
        print("✓ Config imported successfully")
        
        # Test models import
        print("Testing models import...")
        from models.workspace import Workspace, Integration, WorkspaceIntegrationLink
        print("✓ Models imported successfully")
        
        print("\n✓ All basic imports successful!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_fastmcp_basic():
    """Test basic FastMCP functionality"""
    print("\nTesting FastMCP Basic Functionality")
    print("=" * 40)
    
    try:
        from fastmcp import FastMCP
        
        # Create FastMCP instance
        mcp = FastMCP("test-server")
        print("✓ FastMCP instance created")
        
        # Test tool registration
        @mcp.tool()
        def test_tool(message: str) -> str:
            """Test tool that returns a message"""
            return f"Test tool received: {message}"
        
        print("✓ Tool registered successfully")
        
        # Test tool retrieval
        tools = mcp.get_tools()
        print(f"✓ Tools retrieved: {list(tools.keys())}")
        
        # Test tool calling
        result = mcp.call_tool("test_tool", "Hello World")
        print(f"✓ Tool called successfully: {result}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing FastMCP: {e}")
        return False

def test_server_structure():
    """Test server structure without full initialization"""
    print("\nTesting Server Structure")
    print("=" * 25)
    
    try:
        # Test that server files exist and are readable
        server_files = ["gdocs_server.py", "gmail_server.py", "gdrive_server.py", "server.py"]
        
        for server_file in server_files:
            if os.path.exists(server_file):
                print(f"✓ {server_file} exists")
                
                # Check if file contains expected classes
                with open(server_file, 'r') as f:
                    content = f.read()
                    
                if "class" in content and "MCPServer" in content:
                    print(f"✓ {server_file} contains MCP server class")
                else:
                    print(f"⚠ {server_file} may not contain expected MCP server class")
            else:
                print(f"✗ {server_file} not found")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing server structure: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\nTesting Environment Configuration")
    print("=" * 35)
    
    # Check for environment variables
    env_vars = [
        "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET",
        "GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET",
        "GDRIVE_CLIENT_ID", "GDRIVE_CLIENT_SECRET",
        "GDOCS_CLIENT_ID", "GDOCS_CLIENT_SECRET",
        "DATABASE_URL"
    ]
    
    print("Environment Variables:")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: Set")
        else:
            print(f"✗ {var}: Not Set")
    
    # Check for required files
    required_files = [
        "config.py", "fastmcp.py", "models/workspace.py",
        "auth/oauth.py", "database.py"
    ]
    
    print("\nRequired Files:")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}: Exists")
        else:
            print(f"✗ {file_path}: Missing")

def main():
    """Main test function"""
    print("MCP Server Simple Test")
    print("=" * 25)
    
    # Run tests
    imports_ok = test_imports()
    fastmcp_ok = test_fastmcp_basic()
    structure_ok = test_server_structure()
    test_environment()
    
    print("\n" + "=" * 25)
    print("Test Summary")
    print("=" * 25)
    
    if imports_ok and fastmcp_ok and structure_ok:
        print("✓ Basic tests passed!")
        print("\nNext steps:")
        print("1. Install required dependencies:")
        print("   pip install sqlmodel psycopg2-binary google-auth google-auth-oauthlib google-auth-httplib2")
        print("2. Set up environment variables (see env.example)")
        print("3. Run full OAuth tests with: python test_mcp_oauth.py")
    else:
        print("✗ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
