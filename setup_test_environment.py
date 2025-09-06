#!/usr/bin/env python3
"""
Setup script for MCP server testing environment.
This script helps set up the environment for testing the MCP servers.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    
    dependencies = [
        "sqlmodel",
        "psycopg2-binary", 
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "python-dotenv"
    ]
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ {dep} installed")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {dep}")
            return False
    
    return True

def create_env_file():
    """Create .env file template"""
    print("\nCreating .env file template...")
    
    env_content = """# Google OAuth Configuration
# Get these from Google Cloud Console
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Optional: Service-specific credentials
GMAIL_CLIENT_ID=your_gmail_client_id_here
GMAIL_CLIENT_SECRET=your_gmail_client_secret_here
GDRIVE_CLIENT_ID=your_gdrive_client_id_here
GDRIVE_CLIENT_SECRET=your_gdrive_client_secret_here
GDOCS_CLIENT_ID=your_gdocs_client_id_here
GDOCS_CLIENT_SECRET=your_gdocs_client_secret_here

# Database Configuration
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/oneplace_core

# Redirect URI
GOOGLE_REDIRECT_URI=http://localhost:8000/google/callback
"""
    
    if os.path.exists(".env"):
        print("⚠ .env file already exists")
        response = input("Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Skipping .env file creation")
            return True
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✓ .env file created")
        return True
    except Exception as e:
        print(f"✗ Error creating .env file: {e}")
        return False

def test_imports():
    """Test that all imports work"""
    print("\nTesting imports...")
    
    try:
        import sqlmodel
        print("✓ sqlmodel imported")
    except ImportError:
        print("✗ sqlmodel import failed")
        return False
    
    try:
        import google.auth
        print("✓ google.auth imported")
    except ImportError:
        print("✗ google.auth import failed")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv imported")
    except ImportError:
        print("✗ python-dotenv import failed")
        return False
    
    return True

def main():
    """Main setup function"""
    print("MCP Server Test Environment Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        print("Please upgrade Python to 3.8+ and try again")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies. Please install manually:")
        print("pip install sqlmodel psycopg2-binary google-auth google-auth-oauthlib google-auth-httplib2 python-dotenv")
        return
    
    # Create .env file
    if not create_env_file():
        print("Failed to create .env file")
        return
    
    # Test imports
    if not test_imports():
        print("Import test failed. Please check dependencies")
        return
    
    print("\n" + "=" * 40)
    print("Setup Complete!")
    print("=" * 40)
    print("\nNext steps:")
    print("1. Edit .env file with your Google OAuth credentials")
    print("2. Set up PostgreSQL database")
    print("3. Run tests:")
    print("   python simple_test.py")
    print("   python test_mcp_oauth.py")
    print("   python oauth_test_server.py")
    print("\nSee TESTING_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main()
