import asyncio
import json
from typing import Dict, Any, List
from uuid import UUID
from fastmcp import FastMCP
from auth.oauth import GoogleOAuth
from services.gdrive_service import GoogleDriveService
from config import Config
from sqlmodel import Session
from models.workspace import Workspace, Integration, WorkspaceIntegrationLink

class GoogleDriveMCPServer:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        # Initialize Google Drive-specific OAuth
        self.drive_oauth = GoogleOAuth(db_session, "drive")
        self.mcp = FastMCP("gdrive-mcp-server")
        self.setup_tools()
    
    def setup_tools(self):
        """Setup Google Drive-specific MCP tools"""
        
        # Authentication tools for Google Drive
        @self.mcp.tool()
        def get_drive_auth_url() -> str:
            """Get Google OAuth authorization URL for Google Drive access"""
            return self.drive_oauth.get_authorization_url()
        
        @self.mcp.tool()
        def authenticate_drive_user(authorization_code: str, workspace_id: str) -> Dict[str, Any]:
            """Authenticate workspace with authorization code for Google Drive access"""
            try:
                workspace_uuid = UUID(workspace_id)
                return self.drive_oauth.exchange_code_for_tokens(authorization_code, workspace_uuid)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def get_drive_credentials_status(workspace_id: str) -> Dict[str, Any]:
            """Get Google Drive credentials status for a workspace"""
            try:
                workspace_uuid = UUID(workspace_id)
                return self.drive_oauth.get_workspace_credentials_status(workspace_uuid)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        # Google Drive tools
        @self.mcp.tool()
        def list_drive_files(workspace_id: str, page_size: int = 10, query: str = None) -> List[Dict[str, Any]]:
            """List files in Google Drive"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.drive_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return [{"error": "No valid Google Drive credentials found"}]
                
                drive_service = GoogleDriveService(creds)
                return drive_service.list_files(page_size, query)
            except ValueError:
                return [{"error": "Invalid workspace_id format"}]
        
        @self.mcp.tool()
        def create_drive_folder(workspace_id: str, name: str, parent_id: str = None) -> Dict[str, Any]:
            """Create a new folder in Google Drive"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.drive_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return {"error": "No valid Google Drive credentials found"}
                
                drive_service = GoogleDriveService(creds)
                return drive_service.create_folder(name, parent_id)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def upload_drive_file(workspace_id: str, file_path: str, name: str = None, parent_id: str = None) -> Dict[str, Any]:
            """Upload a file to Google Drive"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.drive_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return {"error": "No valid Google Drive credentials found"}
                
                drive_service = GoogleDriveService(creds)
                return drive_service.upload_file(file_path, name, parent_id)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def download_drive_file(workspace_id: str, file_id: str, destination_path: str) -> Dict[str, Any]:
            """Download a file from Google Drive"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.drive_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return {"error": "No valid Google Drive credentials found"}
                
                drive_service = GoogleDriveService(creds)
                return drive_service.download_file(file_id, destination_path)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def share_drive_file(workspace_id: str, file_id: str, email: str, role: str = 'reader') -> Dict[str, Any]:
            """Share a Google Drive file with specific permissions"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.drive_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return {"error": "No valid Google Drive credentials found"}
                
                drive_service = GoogleDriveService(creds)
                return drive_service.share_file(file_id, email, role)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def search_drive_files(workspace_id: str, query: str, page_size: int = 10) -> List[Dict[str, Any]]:
            """Search for files in Google Drive"""
            try:
                workspace_uuid = UUID(workspace_id)
                creds = self.drive_oauth.get_valid_credentials(workspace_uuid)
                if not creds:
                    return [{"error": "No valid Google Drive credentials found"}]
                
                drive_service = GoogleDriveService(creds)
                return drive_service.search_files(query, page_size)
            except ValueError:
                return [{"error": "Invalid workspace_id format"}]
        
        @self.mcp.tool()
        def clear_google_credentials(workspace_id: str) -> Dict[str, Any]:
            """Clear all Google service credentials for a workspace (useful when scopes change)"""
            try:
                workspace_uuid = UUID(workspace_id)
                success = self.drive_oauth.clear_all_credentials_for_workspace(workspace_uuid)
                if success:
                    return {"success": True, "message": "All Google credentials cleared. Re-authorization required."}
                else:
                    return {"error": "Failed to clear credentials"}
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
    from uuid import uuid4
    engine = create_engine("sqlite:///test.db")
    
    # Create tables
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    
    # Create a test workspace with all required fields
    session = Session(engine)
    # workspace = Workspace(
    #     name="Test Drive Workspace",
    #     description="Test workspace for Google Drive",
    #     default_llm_provider=uuid4(),
    #     default_embedding_provider=uuid4(),
    #     default_embedding_model=uuid4(),
    #     default_llm_model=uuid4(),
    #     organization_id=uuid4(),
    #     created_by_id=uuid4()
    # )
    # session.add(workspace)
    # session.commit()
    # session.refresh(workspace)
    
    server = GoogleDriveMCPServer(session)
    asyncio.run(server.start())
