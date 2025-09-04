import asyncio
import json
from typing import Dict, Any, List
from uuid import UUID
from fastmcp import FastMCP
from auth.oauth import GoogleOAuth
from services.gdocs_service import GoogleDocsService
from config import Config
from sqlmodel import Session
from models.workspace import Workspace, Integration, WorkspaceIntegrationLink

class GoogleDocsMCPServer:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        # Initialize Google Docs-specific OAuth
        self.docs_oauth = GoogleOAuth(db_session, "docs")
        self.mcp = FastMCP("gdocs-mcp-server")
        self.setup_tools()
    
    def setup_tools(self):
        """Setup Google Docs-specific MCP tools"""
        
        # Authentication tools for Google Docs
        @self.mcp.tool()
        def get_docs_auth_url() -> str:
            """Get Google OAuth authorization URL for Google Docs access"""
            return self.docs_oauth.get_authorization_url()
        
        @self.mcp.tool()
        def authenticate_docs_user(authorization_code: str, workspace_id: str) -> Dict[str, Any]:
            """Authenticate workspace with authorization code for Google Docs access"""
            try:
                workspace_uuid = UUID(workspace_id)
                return self.docs_oauth.exchange_code_for_tokens(authorization_code, workspace_uuid)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def get_docs_credentials_status(workspace_id: str) -> Dict[str, Any]:
            """Get Google Docs credentials status for a workspace"""
            try:
                workspace_uuid = UUID(workspace_id)
                return self.docs_oauth.get_workspace_credentials_status(workspace_uuid)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        # Google Docs tools
        @self.mcp.tool()
        def create_google_doc(workspace_id: str, title: str, content: str = None) -> Dict[str, Any]:
            """Create a new Google Doc"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.docs_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return {"error": "No valid Google Docs credentials found"}
                
                docs_service = GoogleDocsService(creds)
                return docs_service.create_document(title, content)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def get_google_doc(workspace_id: str, document_id: str) -> Dict[str, Any]:
            """Get content and metadata of a Google Doc"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.docs_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return {"error": "No valid Google Docs credentials found"}
                
                docs_service = GoogleDocsService(creds)
                return docs_service.get_document(document_id)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def update_google_doc(workspace_id: str, document_id: str, content: str, append: bool = False) -> Dict[str, Any]:
            """Update content of a Google Doc"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.docs_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return {"error": "No valid Google Docs credentials found"}
                
                docs_service = GoogleDocsService(creds)
                return docs_service.update_document(document_id, content, append)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def list_google_docs(workspace_id: str, page_size: int = 10) -> List[Dict[str, Any]]:
            """List all Google Docs"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.docs_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return [{"error": "No valid Google Docs credentials found"}]
                
                docs_service = GoogleDocsService(creds)
                return docs_service.list_documents(page_size)
            except ValueError:
                return [{"error": "Invalid workspace_id format"}]
        
        @self.mcp.tool()
        def search_google_docs(workspace_id: str, query: str, page_size: int = 10) -> List[Dict[str, Any]]:
            """Search for Google Docs by content or title"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.docs_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return [{"error": "No valid Google Docs credentials found"}]
                
                docs_service = GoogleDocsService(creds)
                return docs_service.search_documents(query, page_size)
            except ValueError:
                return [{"error": "Invalid workspace_id format"}]
        
        @self.mcp.tool()
        def share_google_doc(workspace_id: str, document_id: str, email: str, role: str = 'reader') -> Dict[str, Any]:
            """Share a Google Doc with specific permissions"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.docs_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return {"error": "No valid Google Docs credentials found"}
                
                docs_service = GoogleDocsService(creds)
                return docs_service.share_document(document_id, email, role)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def export_google_doc(workspace_id: str, document_id: str, export_format: str = 'pdf', output_path: str = None) -> Dict[str, Any]:
            """Export a Google Doc in different formats"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.docs_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return {"error": "No valid Google Docs credentials found"}
                
                docs_service = GoogleDocsService(creds)
                return docs_service.export_document(document_id, export_format, output_path)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
    
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
    workspace = Workspace(name="Test Docs Workspace")
    session.add(workspace)
    session.commit()
    session.refresh(workspace)
    
    server = GoogleDocsMCPServer(session)
    asyncio.run(server.start())
