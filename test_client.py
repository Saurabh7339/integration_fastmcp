import asyncio
import json
from fastmcp import Client

async def test_mcp_client():
    """Test client for the Google Services MCP server"""
    
    # Connect to the MCP server
    client = Client("google-services-mcp")
    
    try:
        # Test authentication flow
        print("=== Testing Authentication ===")
        
        # Get authorization URL
        auth_url = await client.get_auth_url()
        print(f"Authorization URL: {auth_url}")
        print("Please visit this URL to authorize the application")
        
        # In a real scenario, the user would visit the URL and get the authorization code
        # For testing, we'll simulate this
        print("\n=== Simulating OAuth Flow ===")
        print("Note: In a real scenario, you would:")
        print("1. Visit the authorization URL")
        print("2. Grant permissions")
        print("3. Get the authorization code from the redirect")
        print("4. Use that code to authenticate")
        
        # Test credential check (should fail without auth)
        print("\n=== Testing Credential Check ===")
        creds = await client.get_user_credentials()
        print(f"Credentials status: {creds}")
        
        # Test Gmail tools (should fail without auth)
        print("\n=== Testing Gmail Tools (without auth) ===")
        inbox = await client.read_inbox(max_results=5)
        print(f"Inbox result: {inbox}")
        
        # Test Google Drive tools (should fail without auth)
        print("\n=== Testing Google Drive Tools (without auth) ===")
        files = await client.list_drive_files(page_size=5)
        print(f"Drive files result: {files}")
        
        # Test Google Docs tools (should fail without auth)
        print("\n=== Testing Google Docs Tools (without auth) ===")
        docs = await client.list_google_docs(page_size=5)
        print(f"Google Docs result: {docs}")
        
        print("\n=== Test Complete ===")
        print("To fully test the system:")
        print("1. Set up Google OAuth credentials in .env file")
        print("2. Run the server: python server.py")
        print("3. Authenticate a user through the OAuth flow")
        print("4. Test the tools with valid credentials")
        
    except Exception as e:
        print(f"Error during testing: {e}")
    
    finally:
        await client.close()

async def test_with_mock_auth():
    """Test with mock authentication (for demonstration)"""
    
    client = Client("google-services-mcp")
    
    try:
        print("=== Testing with Mock Authentication ===")
        
        # Simulate successful authentication
        print("Simulating successful authentication...")
        
        # Test tool descriptions
        print("\n=== Available Tools ===")
        tools = await client.list_tools()
        for tool in tools:
            print(f"- {tool['name']}: {tool['description']}")
        
        print(f"\nTotal tools available: {len(tools)}")
        
        # Test tool schemas
        print("\n=== Tool Schemas ===")
        for tool in tools[:3]:  # Show first 3 tools
            schema = await client.get_tool_schema(tool['name'])
            print(f"\n{tool['name']}:")
            print(f"  Parameters: {schema.get('parameters', {})}")
        
    except Exception as e:
        print(f"Error during mock testing: {e}")
    
    finally:
        await client.close()

if __name__ == "__main__":
    print("Google Services MCP Test Client")
    print("=" * 40)
    
    # Run basic test
    asyncio.run(test_mcp_client())
    
    print("\n" + "=" * 40)
    
    # Run mock test
    asyncio.run(test_with_mock_auth())
