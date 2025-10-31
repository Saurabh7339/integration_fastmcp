import asyncio
import json
from typing import Dict, Any, List
from uuid import UUID
from fastmcp import FastMCP
from auth.oauth import GoogleOAuth
from database import get_db_session
from services.gdocs_service import GoogleDocsService
from config import Config
from sqlmodel import Session
from models.workspace import Workspace, Integration, WorkspaceIntegrationLink


mcp = FastMCP(
    name="gdocs-mcp-server",
    sse_path="/mcp/sse",
    message_path="/mcp/messages"
)
session = get_db_session()
docs_oauth = GoogleOAuth(session, "docs")

    
# @mcp.tool()
# def get_docs_auth_url() -> str:
#     """Get Google OAuth authorization URL for Google Docs access"""
#     return self.docs_oauth.get_authorization_url()

# @mcp.tool()
# def authenticate_docs_user(authorization_code: str, workspace_id: str) -> Dict[str, Any]:
#     """Authenticate workspace with authorization code for Google Docs access"""
#     try:
#         workspace_uuid = UUID(workspace_id)
#         return self.docs_oauth.exchange_code_for_tokens(authorization_code, workspace_uuid)
#     except ValueError:
#         return {"error": "Invalid workspace_id format"}

# @self.mcp.tool()
# def get_docs_credentials_status(workspace_id: str) -> Dict[str, Any]:
#     """Get Google Docs credentials status for a workspace"""
#     try:
#         workspace_uuid = UUID(workspace_id)
#         return self.docs_oauth.get_workspace_credentials_status(workspace_uuid)
#     except ValueError:
#         return {"error": "Invalid workspace_id format"}

# # Google Docs tools
# #     @mcp.tif __name__ == "__main__":
# # # Use PostgreSQL database configuration
# # from database import get_db_session, create_tables
# # from config import Config

# # # Create tables if they don't exist
# # # create_tables()

# # # Get database session
# # session = get_db_session()

# # try:
# #     server = GoogleDocsMCPServer(session)

# #     # Display available tools
# #     print("Google Docs MCP Server")
# #     print("=" * 30)
# #     print("Available tools:")
# #     tools = server.get_tools()
# #     for tool_name, tool_func in tools.items():
# #         print(f"  - {tool_name}")

# #     print("\nTool descriptions:")
# #     descriptions = server.get_tool_descriptions()
# #     for tool_name, description in descriptions.items():
# #         print(f"  {tool_name}: {description}")

# #     print("\nServer ready. Use the tools through the MCP interface.")

# # finally:
# #     session.close()ool()
@mcp.tool()
def create_google_doc(workspace_id: str, title: str, content: str = None) -> Dict[str, Any]:
    """Create a new Google Doc"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = docs_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return {"error": "No valid Google Docs credentials found"}
        
        docs_service = GoogleDocsService(creds)
        return docs_service.create_document(title, content)
    except ValueError:
        return {"error": "Invalid workspace_id format"}

@mcp.tool()
def get_google_doc(workspace_id: str, document_id: str) -> Dict[str, Any]:
    """Get content and metadata of a Google Doc"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = docs_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return {"error": "No valid Google Docs credentials found"}
        
        docs_service = GoogleDocsService(creds)
        return docs_service.get_document(document_id)
    except ValueError:
        return {"error": "Invalid workspace_id format"}

@mcp.tool()
def update_google_doc(workspace_id: str, document_id: str, content: str, append: bool = False) -> Dict[str, Any]:
    """Update content of a Google Doc"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = docs_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return {"error": "No valid Google Docs credentials found"}
        
        docs_service = GoogleDocsService(creds)
        return docs_service.update_document(document_id, content, append)
    except ValueError:
        return {"error": "Invalid workspace_id format"}

@mcp.tool()
def list_google_docs(workspace_id: str, page_size: int = 10) -> List[Dict[str, Any]]:
    """List all Google Docs"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = docs_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return [{"error": "No valid Google Docs credentials found"}]
        
        docs_service = GoogleDocsService(creds)
        return docs_service.list_documents(page_size)
    except ValueError:
        return [{"error": "Invalid workspace_id format"}]

@mcp.tool()
def search_google_docs(workspace_id: str, query: str, page_size: int = 10) -> List[Dict[str, Any]]:
    """Search for Google Docs by content or title"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = docs_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return [{"error": "No valid Google Docs credentials found"}]
        
        docs_service = GoogleDocsService(creds)
        return docs_service.search_documents(query, page_size)
    except ValueError:
        return [{"error": "Invalid workspace_id format"}]

mcp.tool()
def share_google_doc(workspace_id: str, document_id: str, email: str, role: str = 'reader') -> Dict[str, Any]:
    """Share a Google Doc with specific permissions"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = docs_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return {"error": "No valid Google Docs credentials found"}
    
        docs_service = GoogleDocsService(creds)
        return docs_service.share_document(document_id, email, role)
    except ValueError:
        return {"error": "Invalid workspace_id format"}

mcp.tool()
def export_google_doc(workspace_id: str, document_id: str, export_format: str = 'pdf', output_path: str = None) -> Dict[str, Any]:
    """Export a Google Doc in different formats"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = docs_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return {"error": "No valid Google Docs credentials found"}
    
        docs_service = GoogleDocsService(creds)
        return docs_service.export_document(document_id, export_format, output_path)
    except ValueError:
        return {"error": "Invalid workspace_id format"}

@mcp.tool()
def clear_google_credentials(workspace_id: str) -> Dict[str, Any]:
    """Clear all Google service credentials for a workspace (useful when scopes change)"""
    try:
        workspace_uuid = UUID(workspace_id)
        success = docs_oauth.clear_all_credentials_for_workspace(workspace_uuid)
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


