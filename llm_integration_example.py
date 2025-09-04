#!/usr/bin/env python3
"""
Example showing how LLMs integrate with the MCP servers
This demonstrates the OAuth flow and tool usage patterns.
"""

import asyncio
import json
from typing import Dict, Any

class LLMMCPIntegration:
    """Example LLM integration with MCP servers"""
    
    def __init__(self):
        self.user_id = "user123"
        self.servers = {
            "gmail": "gmail-mcp-server",
            "drive": "gdrive-mcp-server", 
            "docs": "gdocs-mcp-server"
        }
    
    async def authenticate_user(self, service: str) -> Dict[str, Any]:
        """Authenticate user for a specific service"""
        
        print(f"🔐 Authenticating user for {service}...")
        
        # Step 1: Get authorization URL
        auth_url = await self.get_auth_url(service)
        print(f"📋 Authorization URL: {auth_url}")
        
        # Step 2: User completes OAuth (in real scenario, user visits URL)
        print("👤 User needs to visit the authorization URL and complete OAuth")
        print("   After completion, user gets an authorization code")
        
        # Step 3: Exchange code for tokens (simulated)
        auth_code = "4/0AVMBsJ..."  # This would come from user's OAuth completion
        result = await self.exchange_code_for_tokens(service, auth_code)
        
        return result
    
    async def get_auth_url(self, service: str) -> str:
        """Get OAuth authorization URL for a service"""
        
        # LLM would call the MCP tool: get_auth_url
        tool_call = {
            "server": self.servers[service],
            "tool": "get_auth_url",
            "parameters": {
                "user_id": self.user_id
            }
        }
        
        # Simulated response
        return f"https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=http://localhost:8000/auth/callback&scope=..."
    
    async def exchange_code_for_tokens(self, service: str, auth_code: str) -> Dict[str, Any]:
        """Exchange authorization code for access tokens"""
        
        # LLM would call the MCP tool: authenticate_user
        tool_call = {
            "server": self.servers[service],
            "tool": "authenticate_user", 
            "parameters": {
                "user_id": self.user_id,
                "authorization_code": auth_code
            }
        }
        
        # Simulated response
        return {
            "success": True,
            "user_id": self.user_id,
            "message": f"Successfully authenticated for {service}"
        }
    
    async def check_credentials(self, service: str) -> Dict[str, Any]:
        """Check if user has valid credentials for a service"""
        
        # LLM would call the MCP tool: get_user_credentials
        tool_call = {
            "server": self.servers[service],
            "tool": "get_user_credentials",
            "parameters": {
                "user_id": self.user_id
            }
        }
        
        # Simulated response
        return {
            "has_credentials": True,
            "user_id": self.user_id,
            "service": service
        }
    
    async def use_gmail_tools(self) -> Dict[str, Any]:
        """Example of using Gmail tools"""
        
        print("📧 Using Gmail tools...")
        
        # Check credentials first
        creds = await self.check_credentials("gmail")
        if not creds["has_credentials"]:
            await self.authenticate_user("gmail")
        
        # Read inbox
        inbox_result = await self.call_mcp_tool("gmail", "read_inbox", {
            "user_id": self.user_id,
            "max_results": 5
        })
        
        # Search emails
        search_result = await self.call_mcp_tool("gmail", "search_emails", {
            "user_id": self.user_id,
            "query": "from:important@example.com"
        })
        
        return {
            "inbox": inbox_result,
            "search": search_result
        }
    
    async def use_drive_tools(self) -> Dict[str, Any]:
        """Example of using Google Drive tools"""
        
        print("📁 Using Google Drive tools...")
        
        # Check credentials first
        creds = await self.check_credentials("drive")
        if not creds["has_credentials"]:
            await self.authenticate_user("drive")
        
        # List files
        files_result = await self.call_mcp_tool("drive", "list_drive_files", {
            "user_id": self.user_id,
            "page_size": 10
        })
        
        # Create folder
        folder_result = await self.call_mcp_tool("drive", "create_drive_folder", {
            "user_id": self.user_id,
            "folder_name": "LLM Generated Files"
        })
        
        return {
            "files": files_result,
            "new_folder": folder_result
        }
    
    async def use_docs_tools(self) -> Dict[str, Any]:
        """Example of using Google Docs tools"""
        
        print("📝 Using Google Docs tools...")
        
        # Check credentials first
        creds = await self.check_credentials("docs")
        if not creds["has_credentials"]:
            await self.authenticate_user("docs")
        
        # Create document
        create_result = await self.call_mcp_tool("docs", "create_google_doc", {
            "user_id": self.user_id,
            "title": "LLM Generated Document",
            "content": "This document was created by an LLM using MCP tools."
        })
        
        # List documents
        list_result = await self.call_mcp_tool("docs", "list_google_docs", {
            "user_id": self.user_id,
            "page_size": 5
        })
        
        return {
            "new_doc": create_result,
            "documents": list_result
        }
    
    async def call_mcp_tool(self, service: str, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate calling an MCP tool"""
        
        print(f"🛠️  Calling {service} tool: {tool_name}")
        
        # In real implementation, this would be an actual MCP tool call
        tool_call = {
            "server": self.servers[service],
            "tool": tool_name,
            "parameters": parameters
        }
        
        # Simulated response
        return {
            "success": True,
            "tool": tool_name,
            "service": service,
            "data": f"Simulated result from {tool_name}"
        }

async def demonstrate_llm_integration():
    """Demonstrate how an LLM would integrate with the MCP servers"""
    
    print("🤖 LLM MCP Integration Example")
    print("=" * 50)
    print()
    
    llm = LLMMCPIntegration()
    
    # Example 1: Gmail Operations
    print("📧 Example 1: Gmail Operations")
    print("-" * 30)
    gmail_result = await llm.use_gmail_tools()
    print(f"✅ Gmail result: {gmail_result}")
    print()
    
    # Example 2: Google Drive Operations
    print("📁 Example 2: Google Drive Operations")
    print("-" * 30)
    drive_result = await llm.use_drive_tools()
    print(f"✅ Drive result: {drive_result}")
    print()
    
    # Example 3: Google Docs Operations
    print("📝 Example 3: Google Docs Operations")
    print("-" * 30)
    docs_result = await llm.use_docs_tools()
    print(f"✅ Docs result: {docs_result}")
    print()

def show_integration_patterns():
    """Show common integration patterns"""
    
    print("🔧 Common LLM Integration Patterns")
    print("=" * 50)
    print()
    
    print("1️⃣  Authentication Pattern:")
    print("   - Check if user has credentials")
    print("   - If not, get auth URL and guide user through OAuth")
    print("   - Exchange code for tokens")
    print("   - Store credentials for future use")
    print()
    
    print("2️⃣  Tool Usage Pattern:")
    print("   - Always pass user_id to tools")
    print("   - Handle authentication errors gracefully")
    print("   - Use appropriate scopes for each service")
    print()
    
    print("3️⃣  Error Handling Pattern:")
    print("   - Check for expired tokens")
    print("   - Re-authenticate if needed")
    print("   - Provide clear error messages")
    print()
    
    print("4️⃣  Multi-Service Pattern:")
    print("   - Connect to each service independently")
    print("   - Use service-specific namespaces")
    print("   - Combine results from multiple services")
    print()

def show_oauth_flow():
    """Show the complete OAuth flow"""
    
    print("🔐 Complete OAuth Flow for LLMs")
    print("=" * 50)
    print()
    
    print("Step 1: LLM calls get_auth_url")
    print("   → Returns Google authorization URL")
    print()
    
    print("Step 2: User completes OAuth")
    print("   → User visits authorization URL")
    print("   → Signs in with Google")
    print("   → Grants permissions")
    print("   → Gets authorization code")
    print()
    
    print("Step 3: LLM calls authenticate_user")
    print("   → Passes authorization code")
    print("   → Exchanges code for access tokens")
    print("   → Stores tokens securely")
    print()
    
    print("Step 4: LLM uses service tools")
    print("   → Calls tools with user_id")
    print("   → Tokens are automatically used")
    print("   → No need to pass tokens manually")
    print()

def main():
    """Main function"""
    
    print("🤖 LLM MCP Integration Guide")
    print("=" * 60)
    print()
    
    while True:
        print("Choose an option:")
        print("1) 🚀 Run Integration Demo")
        print("2) 🔧 Show Integration Patterns")
        print("3) 🔐 Show OAuth Flow")
        print("4) 🚪 Exit")
        print()
        
        choice = input("Enter your choice (1-4): ").strip()
        print()
        
        if choice == "1":
            asyncio.run(demonstrate_llm_integration())
        elif choice == "2":
            show_integration_patterns()
        elif choice == "3":
            show_oauth_flow()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        print()

if __name__ == "__main__":
    main()
