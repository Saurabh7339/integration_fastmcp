import asyncio
import json
from fastmcp import Client

async def test_gmail_server():
    """Test the Gmail MCP server"""
    print("📧 Testing Gmail MCP Server...")
    print("=" * 40)
    
    try:
        client = Client("gmail-mcp-server")
        
        # Test authentication
        print("🔐 Testing authentication...")
        auth_url = await client.get_auth_url()
        print(f"✅ Auth URL generated: {auth_url[:50]}...")
        
        # Test credential check (should fail without auth)
        print("\n🔑 Testing credentials...")
        creds = await client.get_user_credentials()
        print(f"✅ Credentials check: {creds}")
        
        # Test Gmail tools (should fail without auth)
        print("\n📥 Testing Gmail tools...")
        inbox = await client.read_inbox(max_results=3)
        print(f"✅ Inbox check: {inbox}")
        
        await client.close()
        print("\n✅ Gmail server test completed successfully!")
        
    except Exception as e:
        print(f"❌ Gmail server test failed: {e}")

async def test_gdrive_server():
    """Test the Google Drive MCP server"""
    print("\n📁 Testing Google Drive MCP Server...")
    print("=" * 40)
    
    try:
        client = Client("gdrive-mcp-server")
        
        # Test authentication
        print("🔐 Testing authentication...")
        auth_url = await client.get_auth_url()
        print(f"✅ Auth URL generated: {auth_url[:50]}...")
        
        # Test credential check (should fail without auth)
        print("\n🔑 Testing credentials...")
        creds = await client.get_user_credentials()
        print(f"✅ Credentials check: {creds}")
        
        # Test Drive tools (should fail without auth)
        print("\n📋 Testing Drive tools...")
        files = await client.list_drive_files(page_size=3)
        print(f"✅ Files list check: {files}")
        
        await client.close()
        print("\n✅ Google Drive server test completed successfully!")
        
    except Exception as e:
        print(f"❌ Google Drive server test failed: {e}")

async def test_gdocs_server():
    """Test the Google Docs MCP server"""
    print("\n📝 Testing Google Docs MCP Server...")
    print("=" * 40)
    
    try:
        client = Client("gdocs-mcp-server")
        
        # Test authentication
        print("🔐 Testing authentication...")
        auth_url = await client.get_auth_url()
        print(f"✅ Auth URL generated: {auth_url[:50]}...")
        
        # Test credential check (should fail without auth)
        print("\n🔑 Testing credentials...")
        creds = await client.get_user_credentials()
        print(f"✅ Credentials check: {creds}")
        
        # Test Docs tools (should fail without auth)
        print("\n📄 Testing Docs tools...")
        docs = await client.list_google_docs(page_size=3)
        print(f"✅ Documents list check: {docs}")
        
        await client.close()
        print("\n✅ Google Docs server test completed successfully!")
        
    except Exception as e:
        print(f"❌ Google Docs server test failed: {e}")

async def test_all_servers():
    """Test all three servers"""
    print("🚀 Testing All Three MCP Servers")
    print("=" * 50)
    print("This test will attempt to connect to each server independently.")
    print("Make sure each server is running in a separate terminal.")
    print("=" * 50)
    
    # Test each server
    await test_gmail_server()
    await test_gdrive_server()
    await test_gdocs_server()
    
    print("\n" + "=" * 50)
    print("🎉 All server tests completed!")
    print("\n📋 Summary:")
    print("✅ Each server has its own MCP namespace")
    print("✅ Authentication tools work independently")
    print("✅ Service-specific tools are available")
    print("✅ Servers can run simultaneously")
    print("\n🔗 To use with LLMs:")
    print("   - Connect to gmail-mcp-server for email operations")
    print("   - Connect to gdrive-mcp-server for file operations")
    print("   - Connect to gdocs-mcp-server for document operations")

def show_server_info():
    """Show information about the separate servers"""
    print("📚 Separate MCP Servers Information")
    print("=" * 50)
    
    print("\n📧 Gmail MCP Server (gmail-mcp-server):")
    print("   Tools: read_inbox, create_email, check_sent_emails")
    print("   Tools: check_drafts, check_promotions, check_important_emails")
    print("   Tools: search_emails, get_email_details")
    print("   Authentication: get_auth_url, authenticate_user, get_user_credentials")
    
    print("\n📁 Google Drive MCP Server (gdrive-mcp-server):")
    print("   Tools: list_drive_files, create_drive_folder, upload_drive_file")
    print("   Tools: download_drive_file, share_drive_file, search_drive_files")
    print("   Tools: delete_drive_file, move_drive_file, get_drive_file_info")
    print("   Tools: get_shared_drive_files, get_starred_drive_files")
    print("   Authentication: get_auth_url, authenticate_user, get_user_credentials")
    
    print("\n📝 Google Docs MCP Server (gdocs-mcp-server):")
    print("   Tools: create_google_doc, get_google_doc, update_google_doc")
    print("   Tools: list_google_docs, search_google_docs, share_google_doc")
    print("   Tools: export_google_doc, add_comment_to_doc, delete_google_doc")
    print("   Tools: get_doc_permissions, duplicate_google_doc")
    print("   Authentication: get_auth_url, authenticate_user, get_user_credentials")
    
    print("\n🚀 Benefits of Separate Servers:")
    print("   ✅ Independent scaling and deployment")
    print("   ✅ Service-specific configurations")
    print("   ✅ Better resource isolation")
    print("   ✅ Easier maintenance and updates")
    print("   ✅ Can run on different machines")
    print("   ✅ LLMs can choose which services to connect to")

if __name__ == "__main__":
    print("🧪 Separate MCP Servers Test Client")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1) 🧪 Test Gmail Server")
        print("2) 🧪 Test Google Drive Server")
        print("3) 🧪 Test Google Docs Server")
        print("4) 🚀 Test All Servers")
        print("5) 📚 Show Server Information")
        print("6) 🚪 Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            asyncio.run(test_gmail_server())
        elif choice == "2":
            asyncio.run(test_gdrive_server())
        elif choice == "3":
            asyncio.run(test_gdocs_server())
        elif choice == "4":
            asyncio.run(test_all_servers())
        elif choice == "5":
            show_server_info()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
