import asyncio
import json
from typing import Dict, Any, List
from uuid import UUID
from fastmcp import FastMCP
from auth.oauth import GoogleOAuth
from services.gmail_service import GmailService
from services.gdrive_service import GoogleDriveService
from services.gdocs_service import GoogleDocsService
from config import Config
from sqlmodel import Session, create_engine
from models.workspace import Workspace, Integration, WorkspaceIntegrationLink

class GoogleServicesMCP:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        # Initialize OAuth for each service
        self.gmail_oauth = GoogleOAuth(db_session, "gmail")
        self.drive_oauth = GoogleOAuth(db_session, "drive")
        self.docs_oauth = GoogleOAuth(db_session, "docs")
        self.mcp = FastMCP("google-services-mcp")
        self.setup_tools()
    
    def setup_tools(self):
        """Setup all the MCP tools"""
        
        # Authentication tools for each service
        @self.mcp.tool()
        def get_gmail_auth_url() -> str:
            """Get Google OAuth authorization URL for Gmail access"""
            return self.gmail_oauth.get_authorization_url()
        
        @self.mcp.tool()
        def get_drive_auth_url() -> str:
            """Get Google OAuth authorization URL for Google Drive access"""
            return self.drive_oauth.get_authorization_url()
        
        @self.mcp.tool()
        def get_docs_auth_url() -> str:
            """Get Google OAuth authorization URL for Google Docs access"""
            return self.docs_oauth.get_authorization_url()
        
        @self.mcp.tool()
        def authenticate_gmail_user(authorization_code: str, workspace_id: str) -> Dict[str, Any]:
            """Authenticate workspace with authorization code for Gmail access"""
            try:
                workspace_uuid = UUID(workspace_id)
                return self.gmail_oauth.exchange_code_for_tokens(authorization_code, workspace_uuid)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def authenticate_drive_user(authorization_code: str, workspace_id: str) -> Dict[str, Any]:
            """Authenticate workspace with authorization code for Google Drive access"""
            try:
                workspace_uuid = UUID(workspace_id)
                return self.drive_oauth.exchange_code_for_tokens(authorization_code, workspace_uuid)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def authenticate_docs_user(authorization_code: str, workspace_id: str) -> Dict[str, Any]:
            """Authenticate workspace with authorization code for Google Docs access"""
            try:
                workspace_uuid = UUID(workspace_id)
                return self.docs_oauth.exchange_code_for_tokens(authorization_code, workspace_uuid)
            except ValueError:
                return {"error": "Invalid workspace_id format"}
        
        @self.mcp.tool()
        def get_workspace_credentials_status(workspace_id: str) -> Dict[str, Any]:
            """Get the status of all Google service credentials for a workspace"""
            try:
                workspace_uuid = UUID(workspace_id)
                gmail_status = self.gmail_oauth.get_workspace_credentials_status(workspace_uuid)
                drive_status = self.drive_oauth.get_workspace_credentials_status(workspace_uuid)
                docs_status = self.docs_oauth.get_workspace_credentials_status(workspace_uuid)
                
                return {
                    "workspace_id": workspace_id,
                    "services": {
                        "gmail": gmail_status,
                        "drive": drive_status,
                        "docs": docs_status
                    }
                }
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
    from models.workspace import Workspace
    from sqlmodel import create_engine, Session
    engine = create_engine("sqlite:///test.db")
    Session.bind = engine
    workspace = Workspace(name="Test Workspace")
    session = Session()
    session.add(workspace)
    session.commit()
    session.refresh(workspace)

    server = GoogleServicesMCP(session)
    asyncio.run(server.start())
