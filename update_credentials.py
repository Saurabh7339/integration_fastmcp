#!/usr/bin/env python3
"""
Simple script to update .env file with Google OAuth credentials
"""

import os

def update_credentials():
    print("🔐 Update Google OAuth Credentials")
    print("=" * 40)
    print()
    
    print("📋 You need to get these from Google Cloud Console:")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a project and enable APIs (Gmail, Drive, Docs)")
    print("3. Create OAuth 2.0 credentials (Web application)")
    print("4. Set redirect URI: http://localhost:8000/auth/callback")
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
    
    # Read current .env file
    try:
        with open('.env', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ .env file not found!")
        return
    
    # Replace placeholder values
    content = content.replace('your_google_client_id_here', client_id)
    content = content.replace('your_google_client_secret_here', client_secret)
    
    # Write updated .env file
    try:
        with open('.env', 'w') as f:
            f.write(content)
        
        print()
        print("✅ Credentials updated successfully!")
        print()
        print("🔧 Next steps:")
        print("1. Start the web interface: python3 web_interface.py")
        print("2. Open your browser to: http://localhost:8000")
        print("3. Click 'Start OAuth Authentication'")
        print("4. Complete the Google OAuth flow")
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")

if __name__ == "__main__":
    update_credentials()
