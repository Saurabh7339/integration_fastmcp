import asyncio
import json
from typing import Dict, Any, List
from uuid import UUID
from fastmcp import FastMCP
from auth.oauth import GoogleOAuth
from database import get_db_session
from services.gdrive_service import GoogleDriveService
from config import Config
from sqlmodel import Session
from models.workspace import Workspace, Integration, WorkspaceIntegrationLink

session = get_db_session()
drive_oauth = GoogleOAuth(session, "drive")
mcp = FastMCP(
    name="gdrive-mcp-server",
    sse_path="/mcp/sse",
    message_path="/mcp/messages"
)
    
    # def setup_tools(self):
    #     """Setup Google Drive-specific MCP tools"""
        
    #     # Authentication tools for Google Drive
    #     @self.mcp.tool()
    #     def get_drive_auth_url() -> str:
    #         """Get Google OAuth authorization URL for Google Drive access"""
    #         return self.drive_oauth.get_authorization_url()
        
    #     @self.mcp.tool()
    #     def authenticate_drive_user(authorization_code: str, workspace_id: str) -> Dict[str, Any]:
    #         """Authenticate workspace with authorization code for Google Drive access"""
    #         try:
    #             workspace_uuid = UUID(workspace_id)
    #             return self.drive_oauth.exchange_code_for_tokens(authorization_code, workspace_uuid)
    #         except ValueError:
    #             return {"error": "Invalid workspace_id format"}
        
@mcp.tool()
def get_drive_credentials_status(workspace_id: str) -> Dict[str, Any]:
    """Get Google Drive credentials status for a workspace"""
    try:
        workspace_uuid = UUID(workspace_id)
        return drive_oauth.get_workspace_credentials_status(workspace_uuid)
    except ValueError:
        return {"error": "Invalid workspace_id format"}
        
        # Google Drive tools
@mcp.tool()
def list_drive_files(workspace_id: str, page_size: int = 10, query: str = None) -> List[Dict[str, Any]]:
    """List files in Google Drive"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = drive_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return [{"error": "No valid Google Drive credentials found. Please re-authenticate."}]
        
        drive_service = GoogleDriveService(creds)
        result = drive_service.list_files(page_size, query)
        # Ensure result is always a list
        if isinstance(result, list):
            return result
        else:
            return [{"error": "Unexpected response format from Google Drive service"}]
    except ValueError:
        return [{"error": "Invalid workspace_id format"}]
    except Exception as e:
        return [{"error": f"Error accessing Google Drive: {str(e)}"}]
        
@mcp.tool()
def create_drive_folder(workspace_id: str, name: str, parent_id: str = None) -> Dict[str, Any]:
    """Create a new folder in Google Drive"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = drive_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return {"error": "No valid Google Drive credentials found"}
        
        drive_service = GoogleDriveService(creds)
        return drive_service.create_folder(name, parent_id)
    except ValueError:
        return {"error": "Invalid workspace_id format"}
        
@mcp.tool()
def upload_drive_file(workspace_id: str, file_path: str, name: str = None, parent_id: str = None) -> Dict[str, Any]:
    """Upload a file to Google Drive"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = drive_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return {"error": "No valid Google Drive credentials found"}
        
        drive_service = GoogleDriveService(creds)
        return drive_service.upload_file(file_path, name, parent_id)
    except ValueError:
        return {"error": "Invalid workspace_id format"}
        
@mcp.tool()
def download_drive_file(workspace_id: str, file_id: str, destination_path: str) -> Dict[str, Any]:
    """Download a file from Google Drive"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = drive_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return {"error": "No valid Google Drive credentials found"}
        
        drive_service = GoogleDriveService(creds)
        return drive_service.download_file(file_id, destination_path)
    except ValueError:
        return {"error": "Invalid workspace_id format"}
        
@mcp.tool()
def share_drive_file(workspace_id: str, file_id: str, email: str, role: str = 'reader') -> Dict[str, Any]:
    """Share a Google Drive file with specific permissions"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = drive_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return {"error": "No valid Google Drive credentials found"}
        
        drive_service = GoogleDriveService(creds)
        return drive_service.share_file(file_id, email, role)
    except ValueError:
        return {"error": "Invalid workspace_id format"}

@mcp.tool()
def search_drive_files(workspace_id: str, query: str, page_size: int = 10) -> List[Dict[str, Any]]:
    """Search for files in Google Drive"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = drive_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return [{"error": "No valid Google Drive credentials found"}]
        
        drive_service = GoogleDriveService(creds)
        return drive_service.search_files(query, page_size)
    except ValueError:
        return [{"error": "Invalid workspace_id format"}]
        
@mcp.tool()
def clear_google_credentials(workspace_id: str) -> Dict[str, Any]:
    """Clear all Google service credentials for a workspace (useful when scopes change)"""
    try:
        workspace_uuid = UUID(workspace_id)
        success = drive_oauth.clear_all_credentials_for_workspace(workspace_uuid)
        if success:
            return {"success": True, "message": "All Google credentials cleared. Re-authorization required."}
        else:
            return {"error": "Failed to clear credentials"}
    except ValueError:
        return {"error": "Invalid workspace_id format"}

@mcp.tool()
def check_credentials_status(workspace_id: str) -> Dict[str, Any]:
    """Check the status of Google Drive credentials for a workspace"""
    try:
        workspace_uuid = UUID(workspace_id)
        status = drive_oauth.get_workspace_credentials_status(workspace_uuid)
        return status
    except ValueError:
        return {"error": "Invalid workspace_id format"}
    except Exception as e:
        return {"error": f"Error checking credentials: {str(e)}"}

    # def get_tools(self):
    #     """Get all registered tools"""
    #     return self.mcp.get_tools()
    
    # def get_tool_descriptions(self):
    #     """Get descriptions for all tools"""
    #     return self.mcp.get_tool_descriptions()
    
    # def call_tool(self, tool_name: str, *args, **kwargs):
    #     """Call a specific tool by name"""
    #     return self.mcp.call_tool(tool_name, *args, **kwargs)

# if __name__ == "__main__":
#     # Use PostgreSQL database configuration
#     from database import get_db_session, create_tables
#     from config import Config
    
#     # Create tables if they don't exist
#     # create_tables()
    
#     # Get database session
#     session = get_db_session()
    
#     try:
#         server = GoogleDriveMCPServer(session)
        
#         # Display available tools
#         print("Google Drive MCP Server")
#         print("=" * 25)
#         print("Available tools:")
#         tools = server.get_tools()
#         for tool_name, tool_func in tools.items():
#             print(f"  - {tool_name}")
        
#         print("\nTool descriptions:")
#         descriptions = server.get_tool_descriptions()
#         for tool_name, description in descriptions.items():
#             print(f"  {tool_name}: {description}")
        
#         print("\nServer ready. Use the tools through the MCP interface.")
        
#     finally:
#         session.close()
