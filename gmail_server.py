import asyncio
import json
from typing import Dict, Any, List
from uuid import UUID
from fastmcp import FastMCP
from auth.oauth import GoogleOAuth
from services.gmail_service import GmailService
from config import Config
from sqlmodel import Session
from models.workspace import Workspace, Integration, WorkspaceIntegrationLink

class GmailMCPServer:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        # Initialize Gmail-specific OAuth
        self.gmail_oauth = GoogleOAuth(db_session, "gmail")
        self.mcp = FastMCP("gmail-mcp-server")
        self.setup_tools()
    
    def setup_tools(self):
        """Setup Gmail-specific MCP tools"""
        
        # Authentication tools for Gmail
        @self.mcp.tool()
        def get_gmail_auth_url() -> str:
            """Get Google OAuth authorization URL for Gmail access"""
            return self.gmail_oauth.get_authorization_url()
        
        @self.mcp.tool()
        def authenticate_gmail_user(authorization_code: str, workspace_id: str) -> Dict[str, Any]:
            """Authenticate workspace with authorization code for Gmail access"""
            try:
                workspace_uuid = UUID(workspace_id)
                return self.gmail_oauth.exchange_code_for_tokens(authorization_code, workspace_uuid)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def get_gmail_credentials_status(workspace_id: str) -> Dict[str, Any]:
            """Get Gmail credentials status for a workspace"""
            try:
                workspace_uuid = UUID(workspace_id)
                return self.gmail_oauth.get_workspace_credentials_status(workspace_uuid)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        # Gmail tools
        @self.mcp.tool()
        def read_inbox(workspace_id: str, max_results: int = 10, query: str = None) -> List[Dict[str, Any]]:
            """Read emails from Gmail inbox"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.gmail_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return [{"error": "No valid Gmail credentials found"}]
                
                gmail_service = GmailService(creds)
                return gmail_service.read_inbox(max_results, query)
            except ValueError:
                return [{"error": "Invalid workspace_id format"}]
        
        @self.mcp.tool()
        def create_email(workspace_id: str, to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> Dict[str, Any]:
            """Create and send an email via Gmail"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.gmail_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return {"error": "No valid Gmail credentials found"}
                
                gmail_service = GmailService(creds)
                return gmail_service.create_email(to, subject, body, cc, bcc)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def check_sent_emails(workspace_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
            """Check sent emails in Gmail"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.gmail_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return [{"error": "No valid Gmail credentials found"}]
                
                gmail_service = GmailService(creds)
                return gmail_service.check_sent_emails(max_results)
            except ValueError:
                return [{"error": "Invalid workspace_id format"}]
        
        @self.mcp.tool()
        def check_drafts(workspace_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
            """Check draft emails in Gmail"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.gmail_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return [{"error": "No valid Gmail credentials found"}]
                
                gmail_service = GmailService(creds)
                return gmail_service.check_drafts(max_results)
            except ValueError:
                return [{"error": "Invalid workspace_id format"}]
        
        @self.mcp.tool()
        def check_promotions(workspace_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
            """Check promotional emails in Gmail"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.gmail_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return [{"error": "No valid Gmail credentials found"}]
                
                gmail_service = GmailService(creds)
                return gmail_service.check_promotions(max_results)
            except ValueError:
                return [{"error": "Invalid workspace_id format"}]
        
        @self.mcp.tool()
        def check_important_emails(workspace_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
            """Check important emails in Gmail"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.gmail_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return [{"error": "No valid Gmail credentials found"}]
                
                gmail_service = GmailService(creds)
                return gmail_service.check_important_emails(max_results)
            except ValueError:
                return [{"error": "Invalid workspace_id format"}]
        
        @self.mcp.tool()
        def search_emails(workspace_id: str, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
            """Search emails using Gmail query syntax"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.gmail_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return [{"error": "No valid Gmail credentials found"}]
                
                gmail_service = GmailService(creds)
                return gmail_service.search_emails(query, max_results)
            except ValueError:
                return [{"error": "Invalid workspace_id format"}]
        
        @self.mcp.tool()
        def clear_google_credentials(workspace_id: str) -> Dict[str, Any]:
            """Clear all Google service credentials for a workspace (useful when scopes change)"""
            try:
                workspace_uuid = UUID(workspace_id)
                success = self.gmail_oauth.clear_all_credentials_for_workspace(workspace_uuid)
                if success:
                    return {"success": True, "message": "All Google credentials cleared. Re-authorization required."}
                else:
                    return {"error": "Failed to clear credentials"}
            except ValueError:
                return {"error": "Invalid workspace_id format"}
    
    def get_tools(self):
        """Get all registered tools"""
        return self.mcp.get_tools()
    
    def get_tool_descriptions(self):
        """Get descriptions for all tools"""
        return self.mcp.get_tool_descriptions()
    
    def call_tool(self, tool_name: str, *args, **kwargs):
        """Call a specific tool by name"""
        return self.mcp.call_tool(tool_name, *args, **kwargs)

if __name__ == "__main__":
    # Use PostgreSQL database configuration
    from database import get_db_session, create_tables
    from config import Config
    
    # Create tables if they don't exist
    # create_tables()
    
    # Get database session
    session = get_db_session()
    
    try:
        server = GmailMCPServer(session)
        
        # Display available tools
        print("Gmail MCP Server")
        print("=" * 20)
        print("Available tools:")
        tools = server.get_tools()
        for tool_name, tool_func in tools.items():
            print(f"  - {tool_name}")
        
        print("\nTool descriptions:")
        descriptions = server.get_tool_descriptions()
        for tool_name, description in descriptions.items():
            print(f"  {tool_name}: {description}")
        
        print("\nServer ready. Use the tools through the MCP interface.")
        
    finally:
        session.close()
