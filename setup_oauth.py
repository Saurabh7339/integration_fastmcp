#!/usr/bin/env python3
"""
OAuth Setup Script for FastMCP Google Services
This script helps you create the .env file with your Google OAuth credentials.
"""

import os
import secrets

def create_env_file():
    """Create the .env file with OAuth configuration"""
    
    print("🔐 Google OAuth Setup for FastMCP")
    print("=" * 50)
    print()
    
    print("📋 Prerequisites:")
    print("1. You need a Google Cloud Project")
    print("2. You need OAuth 2.0 credentials")
    print("3. You need to enable Gmail, Drive, and Docs APIs")
    print()
    
    print("🌐 If you haven't set up Google Cloud yet:")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a new project")
    print("3. Enable Gmail API, Drive API, and Docs API")
    print("4. Create OAuth 2.0 credentials")
    print("5. Set redirect URI to: http://localhost:8000/auth/callback")
    print()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    print("📝 Enter your Google OAuth credentials:")
    print()
    
    # Get credentials from user
    client_id = input("Enter your Google Client ID: ").strip()
    if not client_id:
        print("❌ Client ID is required!")
        return
    
    client_secret = input("Enter your Google Client Secret: ").strip()
    if not client_secret:
        print("❌ Client Secret is required!")
        return
    
    # Generate a random secret key
    secret_key = secrets.token_urlsafe(32)
    
    # Create .env content
    env_content = f"""# Google OAuth Configuration
GOOGLE_CLIENT_ID={client_id}
GOOGLE_CLIENT_SECRET={client_secret}
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# Google API Scopes
GMAIL_SCOPE=https://www.googleapis.com/auth/gmail.modify
GDRIVE_SCOPE=https://www.googleapis.com/auth/drive
GDOCS_SCOPE=https://www.googleapis.com/auth/documents

# Server Configuration
HOST=0.0.0.0
PORT=8000
SECRET_KEY={secret_key}
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print()
        print("✅ .env file created successfully!")
        print()
        print("🔧 Next steps:")
        print("1. Start the web interface: python3 web_interface.py")
        print("2. Open your browser to: http://localhost:8000")
        print("3. Click 'Start OAuth Authentication'")
        print("4. Complete the Google OAuth flow")
        print("5. Test the tools!")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def show_help():
    """Show help information"""
    print("🔐 Google OAuth Setup Help")
    print("=" * 40)
    print()
    print("📋 What you need:")
    print("1. Google Cloud Project")
    print("2. OAuth 2.0 Client ID and Secret")
    print("3. Enabled APIs (Gmail, Drive, Docs)")
    print()
    print("🌐 Setup Steps:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project")
    print("3. Enable APIs: Gmail, Drive, Docs")
    print("4. Create OAuth 2.0 credentials")
    print("5. Set redirect URI: http://localhost:8000/auth/callback")
    print("6. Run this script to create .env file")
    print()
    print("🔧 After setup:")
    print("1. python3 web_interface.py")
    print("2. Open http://localhost:8000")
    print("3. Test OAuth and tools")

def main():
    """Main function"""
    print("🔐 FastMCP Google OAuth Setup")
    print("=" * 40)
    print()
    
    while True:
        print("Choose an option:")
        print("1) 🚀 Create .env file")
        print("2) 📚 Show help")
        print("3) 🚪 Exit")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        print()
        
        if choice == "1":
            create_env_file()
            break
        elif choice == "2":
            show_help()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        print()

if __name__ == "__main__":
    main()
