import asyncio
import json
from typing import Dict, Any, List
from uuid import UUID
from fastmcp import FastMCP
from auth.oauth import GoogleOAuth
from database import get_db_session
from services.gmail_service import GmailService
from config import Config
from sqlmodel import Session
from models.workspace import Workspace, Integration, WorkspaceIntegrationLink

session = get_db_session()
gmail_oauth = GoogleOAuth(session, "gmail")
mcp = FastMCP(
    name="gdrive-mcp-server",
    sse_path="/mcp/sse",
    message_path="/mcp/messages"
)
    
    
    # def setup_tools(self):
    #     """Setup Gmail-specific MCP tools"""
        
    #     # Authentication tools for Gmail
    #     @self.mcp.tool()
    #     def get_gmail_auth_url() -> str:
    #         """
    #         Get Google OAuth authorization URL for Gmail access.
            
    #         This tool generates a Google OAuth authorization URL that users can visit to grant
    #         permission for the application to access their Gmail account. The URL includes
    #         the necessary scopes for Gmail operations.
            
    #         Returns:
    #             str: A complete OAuth authorization URL that can be opened in a web browser.
    #                  Users will be redirected to Google's consent screen to authorize access.
            
    #         Example:
    #             url = get_gmail_auth_url()
    #             # Returns: "https://accounts.google.com/o/oauth2/auth?client_id=..."
    #         """
    #         return self.gmail_oauth.get_authorization_url()
        
    #     @self.mcp.tool()
    #     def authenticate_gmail_user(authorization_code: str, workspace_id: str) -> Dict[str, Any]:
    #         """
    #         Authenticate workspace with authorization code for Gmail access.
            
    #         This tool exchanges an authorization code (obtained from the OAuth flow) for
    #         access and refresh tokens, then stores them securely in the database for the
    #         specified workspace. This completes the OAuth authentication process.
            
    #         Parameters:
    #             authorization_code (str): The authorization code received from Google OAuth callback.
    #                                     This is obtained after the user authorizes the application
    #                                     and is redirected back with the code in the URL.
    #             workspace_id (str): The UUID of the workspace to associate the credentials with.
    #                               Must be a valid UUID string format.
            
    #         Returns:
    #             Dict[str, Any]: Authentication result containing:
    #                 - success (bool): Whether authentication was successful
    #                 - service_type (str): "gmail" 
    #                 - access_token (str): Short-lived access token for API calls
    #                 - refresh_token (str): Long-lived token for refreshing access
    #                 - expires_at (str): ISO timestamp when access token expires
    #                 - error (str): Error message if authentication failed
            
    #         Example:
    #             result = authenticate_gmail_user("4/0AVMBsJi8Evs4kPEaPRHMcw6NCB8o26B2tPpp7FJOviJ49JBTQGaXSh0u3krcg-WQUx7upg", 
    #                                            "550e8400-e29b-41d4-a716-446655440000")
    #         """
    #         try:
    #             workspace_uuid = UUID(workspace_id)
    #             return self.gmail_oauth.exchange_code_for_tokens(authorization_code, workspace_uuid)
    #         except ValueError:
    #             return {"error": "Invalid workspace_id format"}
        
    #     @self.mcp.tool()
    #     def get_gmail_credentials_status(workspace_id: str) -> Dict[str, Any]:
    #         """
    #         Get Gmail credentials status for a workspace.
            
    #         This tool checks whether valid Gmail credentials exist for the specified workspace
    #         and provides information about the current authentication status, including
    #         token expiration and scope information.
            
    #         Parameters:
    #             workspace_id (str): The UUID of the workspace to check credentials for.
    #                               Must be a valid UUID string format.
            
    #         Returns:
    #             Dict[str, Any]: Credentials status containing:
    #                 - has_credentials (bool): Whether valid credentials exist
    #                 - service_type (str): "gmail"
    #                 - integration_id (str): UUID of the Gmail integration
    #                 - integration_name (str): Name of the integration
    #                 - created_date (str): ISO timestamp when credentials were created
    #                 - scopes (list): List of OAuth scopes granted
    #                 - expires_at (str): ISO timestamp when access token expires
    #                 - error (str): Error message if check failed
            
    #         Example:
    #             status = get_gmail_credentials_status("550e8400-e29b-41d4-a716-446655440000")
    #             if status.get("has_credentials"):
    #                 print("Gmail is authenticated and ready to use")
    #         """
    #         try:
    #             workspace_uuid = UUID(workspace_id)
    #             return self.gmail_oauth.get_workspace_credentials_status(workspace_uuid)
    #         except ValueError:
    #             return {"error": "Invalid workspace_id format"}
        
        # Gmail tools
@mcp.tool()
def read_inbox(workspace_id: str, max_results: int = 10, query: str = None) -> List[Dict[str, Any]]:
    """Read emails from Gmail inbox"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = gmail_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return [{"error": "No valid Gmail credentials found"}]
        
        gmail_service = GmailService(creds)
        return gmail_service.read_inbox(max_results, query)
    except ValueError:
        return [{"error": "Invalid workspace_id format"}]
        
@mcp.tool()
def create_email(workspace_id: str, to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> Dict[str, Any]:
    """Create and send an email via Gmail"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = gmail_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return {"error": "No valid Gmail credentials found"}
        
        gmail_service = GmailService(creds)
        return gmail_service.create_email(to, subject, body, cc, bcc)
    except ValueError:
        return {"error": "Invalid workspace_id format"}
        
@mcp.tool()
def check_sent_emails(workspace_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Check sent emails in Gmail"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = gmail_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return [{"error": "No valid Gmail credentials found"}]
        
        gmail_service = GmailService(creds)
        return gmail_service.check_sent_emails(max_results)
    except ValueError:
        return [{"error": "Invalid workspace_id format"}]
        
@mcp.tool()
def check_drafts(workspace_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Check draft emails in Gmail"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = gmail_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return [{"error": "No valid Gmail credentials found"}]
        
        gmail_service = GmailService(creds)
        return gmail_service.check_drafts(max_results)
    except ValueError:
        return [{"error": "Invalid workspace_id format"}]
        
@mcp.tool()
def check_promotions(workspace_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Check promotional emails in Gmail"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = gmail_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return [{"error": "No valid Gmail credentials found"}]
        
        gmail_service = GmailService(creds)
        return gmail_service.check_promotions(max_results)
    except ValueError:
        return [{"error": "Invalid workspace_id format"}]
        
@mcp.tool()
def check_important_emails(workspace_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Check important emails in Gmail"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = gmail_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return [{"error": "No valid Gmail credentials found"}]
        
        gmail_service = GmailService(creds)
        return gmail_service.check_important_emails(max_results)
    except ValueError:
        return [{"error": "Invalid workspace_id format"}]

@mcp.tool()
def search_emails(workspace_id: str, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Search emails using Gmail query syntax"""
    try:
        workspace_uuid = UUID(workspace_id)
        creds = gmail_oauth.get_valid_credentials(workspace_uuid)
        if not creds:
            return [{"error": "No valid Gmail credentials found"}]
        
        gmail_service = GmailService(creds)
        return gmail_service.search_emails(query, max_results)
    except ValueError:
        return [{"error": "Invalid workspace_id format"}]
        
@mcp.tool()
def clear_google_credentials(workspace_id: str) -> Dict[str, Any]:
    """Clear all Google service credentials for a workspace (useful when scopes change)"""
    try:
        workspace_uuid = UUID(workspace_id)
        success = gmail_oauth.clear_all_credentials_for_workspace(workspace_uuid)
        if success:
            return {"success": True, "message": "All Google credentials cleared. Re-authorization required."}
        else:
            return {"error": "Failed to clear credentials"}
    except ValueError:
        return {"error": "Invalid workspace_id format"}
    
#     def get_tools(self):
#         """Get all registered tools"""
#         return self.mcp.get_tools()
    
#     def get_tool_descriptions(self):
#         """Get descriptions for all tools"""
#         return self.mcp.get_tool_descriptions()
    
#     def call_tool(self, tool_name: str, *args, **kwargs):
#         """Call a specific tool by name"""
#         return self.mcp.call_tool(tool_name, *args, **kwargs)

# if __name__ == "__main__":
#     # Use PostgreSQL database configuration
#     from database import get_db_session, create_tables
#     from config import Config
    
#     # Create tables if they don't exist
#     # create_tables()
    
#     # Get database session
#     session = get_db_session()
    
#     try:
#         server = GmailMCPServer(session)
        
#         # Display available tools
#         print("Gmail MCP Server")
#         print("=" * 20)
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
