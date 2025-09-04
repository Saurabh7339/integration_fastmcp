#!/usr/bin/env python3
"""
Example usage of the service-specific database-integrated OAuth system with SQLite
"""

import asyncio
from uuid import UUID
from database import create_tables, create_workspace, get_db_session
from auth.oauth import GoogleOAuth
from server import GoogleServicesMCP

async def main():
    """Main example function"""
    print("🚀 Setting up service-specific database-integrated OAuth system with SQLite...")
    
    # Create database tables
    create_tables()
    print("✅ SQLite database tables created")
    
    # Create a test workspace
    workspace = create_workspace("Example Workspace")
    if workspace:
        print(f"✅ Created workspace: {workspace['name']} (ID: {workspace['id']})")
        workspace_id = workspace['id']
    else:
        print("❌ Failed to create workspace")
        return
    
    # Get database session
    db_session = get_db_session()
    
    # Initialize OAuth for each service
    gmail_oauth = GoogleOAuth(db_session, "gmail")
    drive_oauth = GoogleOAuth(db_session, "drive")
    docs_oauth = GoogleOAuth(db_session, "docs")
    print("✅ Service-specific OAuth systems initialized")
    
    # Get authorization URLs for each service
    gmail_auth_url = gmail_oauth.get_authorization_url()
    drive_auth_url = drive_oauth.get_authorization_url()
    docs_auth_url = docs_oauth.get_authorization_url()
    
    print(f"\n🔗 Authorization URLs:")
    print(f"   Gmail: {gmail_auth_url}")
    print(f"   Drive: {drive_auth_url}")
    print(f"   Docs:  {docs_auth_url}")
    
    # Check workspace credentials status for each service
    print(f"\n📊 Credentials status for workspace {workspace_id}:")
    
    gmail_status = gmail_oauth.get_workspace_credentials_status(UUID(workspace_id))
    drive_status = drive_oauth.get_workspace_credentials_status(UUID(workspace_id))
    docs_status = docs_oauth.get_workspace_credentials_status(UUID(workspace_id))
    
    print(f"   Gmail: {gmail_status['has_credentials']}")
    print(f"   Drive: {drive_status['has_credentials']}")
    print(f"   Docs:  {docs_status['has_credentials']}")
    
    # Initialize MCP server
    mcp_server = GoogleServicesMCP(db_session)
    print("✅ MCP server initialized with service-specific OAuth")
    
    # Example of checking all service credentials
    print("\n🔍 Checking all workspace service credentials...")
    all_creds = mcp_server.get_workspace_credentials_status(workspace_id)
    print(f"All credentials status: {all_creds}")
    
    print("\n📋 Available MCP tools:")
    print("\n🔐 Authentication tools:")
    print("   - get_gmail_auth_url: Get OAuth URL for Gmail")
    print("   - get_drive_auth_url: Get OAuth URL for Google Drive")
    print("   - get_docs_auth_url: Get OAuth URL for Google Docs")
    print("   - authenticate_gmail_user: Complete Gmail OAuth flow")
    print("   - authenticate_drive_user: Complete Drive OAuth flow")
    print("   - authenticate_docs_user: Complete Docs OAuth flow")
    print("   - get_workspace_credentials_status: Check all service credentials")
    
    print("\n📧 Gmail tools (require Gmail credentials):")
    print("   - read_inbox: Read emails from Gmail inbox")
    print("   - create_email: Send emails")
    print("   - check_sent_emails: View sent emails")
    print("   - check_drafts: View draft emails")
    print("   - check_promotions: View promotional emails")
    print("   - check_important_emails: View important emails")
    print("   - search_emails: Search emails")
    
    print("\n📁 Google Drive tools (require Drive credentials):")
    print("   - list_drive_files: List files and folders")
    print("   - create_drive_folder: Create new folders")
    print("   - upload_drive_file: Upload files")
    print("   - download_drive_file: Download files")
    print("   - share_drive_file: Share files")
    print("   - search_drive_files: Search for files")
    
    print("\n📝 Google Docs tools (require Docs credentials):")
    print("   - create_google_doc: Create new documents")
    print("   - get_google_doc: Read document content")
    print("   - update_google_doc: Edit documents")
    print("   - list_google_docs: Browse all documents")
    print("   - search_google_docs: Search documents")
    print("   - share_google_doc: Share documents")
    print("   - export_google_doc: Export to different formats")
    
    print(f"\n💡 To use any service, you'll need to:")
    print(f"   1. Use the appropriate authorization URL for the service you want")
    print(f"   2. Complete OAuth flow for that specific service")
    print(f"   3. Call the appropriate authenticate function with your authorization code and workspace_id: {workspace_id}")
    print(f"   4. Use any service function with the workspace_id: {workspace_id}")
    
    print(f"\n🎯 Key Benefits of Service-Specific Integrations:")
    print(f"   - Each service (Gmail, Drive, Docs) has separate OAuth credentials")
    print(f"   - Workspaces can choose which services to connect to")
    print(f"   - Granular access control per service")
    print(f"   - Independent token refresh for each service")
    print(f"   - Better security isolation between services")
    
    print(f"\n🗄️ Database structure:")
    print(f"   - Integration table: Google Gmail, Google Drive, Google Docs")
    print(f"   - WorkspaceIntegrationLink: Links workspaces to specific services")
    print(f"   - Each service has its own OAuth credentials and refresh tokens")
    
    print(f"\n🗄️ Database file created: fastmcp.db")
    print("   - This SQLite database contains your workspaces and service-specific OAuth credentials")
    print("   - You can inspect it using any SQLite browser")
    
    # Close database session
    db_session.close()

if __name__ == "__main__":
    asyncio.run(main())
