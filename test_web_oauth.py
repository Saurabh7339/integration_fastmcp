#!/usr/bin/env python3
"""
Web-based OAuth test script for MCP servers.
This script provides a simple web interface to test the OAuth flow
for Google Docs, Gmail, and Google Drive MCP servers.
"""

import asyncio
import json
import os
import sys
from uuid import uuid4
from database import get_db_session, create_tables
from config import Config

# Import servers
from gdocs_server import GoogleDocsMCPServer
from gmail_server import GmailMCPServer
from gdrive_server import GoogleDriveMCPServer

class OAuthTestInterface:
    def __init__(self):
        self.session = get_db_session()
        self.docs_server = GoogleDocsMCPServer(self.session)
        self.gmail_server = GmailMCPServer(self.session)
        self.drive_server = GoogleDriveMCPServer(self.session)
        self.test_workspace_id = self._get_or_create_test_workspace()
    
    def _get_or_create_test_workspace(self):
        """Get or create a test workspace"""
        try:
            from database import get_or_create_workspace
            workspace = get_or_create_workspace("test_workspace")
            return workspace["id"]
        except Exception as e:
            print(f"Warning: Could not create workspace, using random UUID: {e}")
            return str(uuid4())
    
    def get_oauth_urls(self):
        """Get OAuth URLs for all services"""
        try:
            docs_url = self.docs_server.call_tool("get_docs_auth_url")
            gmail_url = self.gmail_server.call_tool("get_gmail_auth_url")
            drive_url = self.drive_server.call_tool("get_drive_auth_url")
            
            return {
                "docs": docs_url,
                "gmail": gmail_url,
                "drive": drive_url
            }
        except Exception as e:
            return {"error": str(e)}
    
    def test_oauth_flow(self, service, auth_code):
        """Test OAuth flow with authorization code"""
        try:
            if service == "docs":
                result = self.docs_server.call_tool("authenticate_docs_user", auth_code, self.test_workspace_id)
            elif service == "gmail":
                result = self.gmail_server.call_tool("authenticate_gmail_user", auth_code, self.test_workspace_id)
            elif service == "drive":
                result = self.drive_server.call_tool("authenticate_drive_user", auth_code, self.test_workspace_id)
            else:
                return {"error": f"Unknown service: {service}"}
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def get_credentials_status(self, service):
        """Get credentials status for a service"""
        try:
            if service == "docs":
                result = self.docs_server.call_tool("get_docs_credentials_status", self.test_workspace_id)
            elif service == "gmail":
                result = self.gmail_server.call_tool("get_gmail_credentials_status", self.test_workspace_id)
            elif service == "drive":
                result = self.drive_server.call_tool("get_drive_credentials_status", self.test_workspace_id)
            else:
                return {"error": f"Unknown service: {service}"}
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def test_service_tools(self, service):
        """Test service tools"""
        try:
            if service == "docs":
                result = self.docs_server.call_tool("list_google_docs", self.test_workspace_id)
            elif service == "gmail":
                result = self.gmail_server.call_tool("read_inbox", self.test_workspace_id)
            elif service == "drive":
                result = self.drive_server.call_tool("list_drive_files", self.test_workspace_id)
            else:
                return {"error": f"Unknown service: {service}"}
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def clear_credentials(self, service):
        """Clear credentials for a service"""
        try:
            if service == "docs":
                result = self.docs_server.call_tool("clear_google_credentials", self.test_workspace_id)
            elif service == "gmail":
                result = self.gmail_server.call_tool("clear_google_credentials", self.test_workspace_id)
            elif service == "drive":
                result = self.drive_server.call_tool("clear_google_credentials", self.test_workspace_id)
            else:
                return {"error": f"Unknown service: {service}"}
            
            return result
        except Exception as e:
            return {"error": str(e)}

def interactive_test():
    """Interactive test interface"""
    print("MCP Server OAuth Interactive Test")
    print("=" * 40)
    
    # Initialize test interface
    try:
        create_tables()
        test_interface = OAuthTestInterface()
        print("✓ Test interface initialized")
    except Exception as e:
        print(f"✗ Error initializing test interface: {e}")
        return
    
    while True:
        print("\nOptions:")
        print("1. Get OAuth URLs")
        print("2. Test OAuth flow")
        print("3. Check credentials status")
        print("4. Test service tools")
        print("5. Clear credentials")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            print("\nGetting OAuth URLs...")
            urls = test_interface.get_oauth_urls()
            if "error" in urls:
                print(f"✗ Error: {urls['error']}")
            else:
                print("✓ OAuth URLs generated:")
                for service, url in urls.items():
                    print(f"  {service.upper()}: {url}")
        
        elif choice == "2":
            service = input("Enter service (docs/gmail/drive): ").strip().lower()
            auth_code = input("Enter authorization code: ").strip()
            
            if service not in ["docs", "gmail", "drive"]:
                print("✗ Invalid service")
                continue
            
            print(f"\nTesting OAuth flow for {service}...")
            result = test_interface.test_oauth_flow(service, auth_code)
            print(f"Result: {json.dumps(result, indent=2)}")
        
        elif choice == "3":
            service = input("Enter service (docs/gmail/drive): ").strip().lower()
            
            if service not in ["docs", "gmail", "drive"]:
                print("✗ Invalid service")
                continue
            
            print(f"\nChecking credentials status for {service}...")
            result = test_interface.get_credentials_status(service)
            print(f"Result: {json.dumps(result, indent=2)}")
        
        elif choice == "4":
            service = input("Enter service (docs/gmail/drive): ").strip().lower()
            
            if service not in ["docs", "gmail", "drive"]:
                print("✗ Invalid service")
                continue
            
            print(f"\nTesting service tools for {service}...")
            result = test_interface.test_service_tools(service)
            print(f"Result: {json.dumps(result, indent=2)}")
        
        elif choice == "5":
            service = input("Enter service (docs/gmail/drive): ").strip().lower()
            
            if service not in ["docs", "gmail", "drive"]:
                print("✗ Invalid service")
                continue
            
            print(f"\nClearing credentials for {service}...")
            result = test_interface.clear_credentials(service)
            print(f"Result: {json.dumps(result, indent=2)}")
        
        elif choice == "6":
            print("Exiting...")
            break
        
        else:
            print("✗ Invalid choice")

def main():
    """Main function"""
    print("MCP Server OAuth Web Test")
    print("=" * 30)
    
    # Check environment
    print("Checking environment configuration...")
    required_vars = ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"✗ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before running the test.")
        return
    
    print("✓ Environment configuration OK")
    
    # Run interactive test
    interactive_test()

if __name__ == "__main__":
    main()
