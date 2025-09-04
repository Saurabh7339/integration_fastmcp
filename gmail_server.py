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
    
    async def start(self):
        """Start the MCP server"""
        await self.mcp.start()
    
    async def stop(self):
        """Stop the MCP server"""
        await self.mcp.stop()

if __name__ == "__main__":
    # For demonstration, create a dummy database session
    from sqlmodel import create_engine, Session
    engine = create_engine("sqlite:///test.db")
    Session.bind = engine
    
    # Create a test workspace
    session = Session()
    workspace = Workspace(name="Test Gmail Workspace")
    session.add(workspace)
    session.commit()
    session.refresh(workspace)
    
    server = GmailMCPServer(session)
    asyncio.run(server.start())
