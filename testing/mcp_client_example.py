#!/usr/bin/env python3
"""
Example script showing how to connect to the MCP servers
This demonstrates the proper way to connect to the running servers.
"""

import subprocess
import json
import sys
import os

def send_mcp_request(server_process, method, params=None):
    """Send an MCP request to a server process"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    
    try:
        # Send request
        server_process.stdin.write(json.dumps(request) + "\n")
        server_process.stdin.flush()
        
        # Read response
        response_line = server_process.stdout.readline()
        if response_line:
            return json.loads(response_line)
        else:
            return None
    except Exception as e:
        print(f"Error sending request: {e}")
        return None

def test_gmail_server():
    """Test the Gmail server"""
    print("📧 Testing Gmail MCP Server")
    print("=" * 40)
    
    try:
        # Start the Gmail server
        server_process = subprocess.Popen(
            [sys.executable, "gmail_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Wait for server to start
        import time
        time.sleep(3)
        
        # Test server initialization
        print("✅ Gmail server started")
        print(f"📊 Process ID: {server_process.pid}")
        
        # Test basic MCP communication
        print("\n🔍 Testing MCP communication...")
        
        # Send an initialization request
        init_response = send_mcp_request(server_process, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        
        if init_response:
            print("✅ MCP initialization successful")
            print(f"📋 Server info: {init_response.get('result', {}).get('serverInfo', {})}")
        else:
            print("❌ MCP initialization failed")
        
        # Clean up
        server_process.terminate()
        server_process.wait(timeout=5)
        print("✅ Gmail server shut down cleanly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gmail server: {e}")
        return False

def show_connection_guide():
    """Show how to connect to the servers"""
    print("🔗 How to Connect to MCP Servers")
    print("=" * 50)
    
    print("\n📋 Server Information:")
    print("   Gmail Server: gmail-mcp-server")
    print("   Drive Server: gdrive-mcp-server")
    print("   Docs Server: gdocs-mcp-server")
    
    print("\n🚀 Starting Servers:")
    print("   # Terminal 1")
    print("   python3 gmail_server.py")
    print()
    print("   # Terminal 2")
    print("   python3 gdrive_server.py")
    print()
    print("   # Terminal 3")
    print("   python3 gdocs_server.py")
    
    print("\n🔧 Transport Method:")
    print("   All servers use STDIO transport")
    print("   They communicate via stdin/stdout")
    print("   Each server runs independently")
    
    print("\n🤖 LLM Integration:")
    print("   LLMs should connect to each server separately")
    print("   Use the server namespaces for identification")
    print("   Each server has its own OAuth flow")
    
    print("\n📝 Example Usage:")
    print("   # For email operations")
    print("   Connect to: gmail-mcp-server")
    print("   Use tools: read_inbox, create_email")
    print()
    print("   # For file operations")
    print("   Connect to: gdrive-mcp-server")
    print("   Use tools: list_drive_files, upload_drive_file")
    print()
    print("   # For document operations")
    print("   Connect to: gdocs-mcp-server")
    print("   Use tools: create_google_doc, update_google_doc")

def show_available_tools():
    """Show available tools for each server"""
    print("🛠️ Available Tools by Server")
    print("=" * 50)
    
    print("\n📧 Gmail Server (gmail-mcp-server):")
    print("   Authentication:")
    print("     • get_auth_url")
    print("     • authenticate_user")
    print("     • get_user_credentials")
    print("   Email Operations:")
    print("     • read_inbox")
    print("     • create_email")
    print("     • check_sent_emails")
    print("     • check_drafts")
    print("     • check_promotions")
    print("     • check_important_emails")
    print("     • search_emails")
    print("     • get_email_details")
    
    print("\n📁 Google Drive Server (gdrive-mcp-server):")
    print("   Authentication:")
    print("     • get_auth_url")
    print("     • authenticate_user")
    print("     • get_user_credentials")
    print("   File Operations:")
    print("     • list_drive_files")
    print("     • create_drive_folder")
    print("     • upload_drive_file")
    print("     • download_drive_file")
    print("     • share_drive_file")
    print("     • search_drive_files")
    print("     • delete_drive_file")
    print("     • move_drive_file")
    print("     • get_drive_file_info")
    print("     • get_shared_drive_files")
    print("     • get_starred_drive_files")
    
    print("\n📝 Google Docs Server (gdocs-mcp-server):")
    print("   Authentication:")
    print("     • get_auth_url")
    print("     • authenticate_user")
    print("     • get_user_credentials")
    print("   Document Operations:")
    print("     • create_google_doc")
    print("     • get_google_doc")
    print("     • update_google_doc")
    print("     • list_google_docs")
    print("     • search_google_docs")
    print("     • share_google_doc")
    print("     • export_google_doc")
    print("     • add_comment_to_doc")
    print("     • delete_google_doc")
    print("     • get_doc_permissions")
    print("     • duplicate_google_doc")

def main():
    """Main function"""
    print("🔗 MCP Server Connection Example")
    print("=" * 60)
    print()
    
    while True:
        print("Choose an option:")
        print("1) 🧪 Test Gmail Server Connection")
        print("2) 🔗 Show Connection Guide")
        print("3) 🛠️ Show Available Tools")
        print("4) 🚪 Exit")
        print()
        
        choice = input("Enter your choice (1-4): ").strip()
        print()
        
        if choice == "1":
            success = test_gmail_server()
            if success:
                print("\n✅ Gmail server test completed successfully!")
            else:
                print("\n❌ Gmail server test failed!")
        
        elif choice == "2":
            show_connection_guide()
        
        elif choice == "3":
            show_available_tools()
        
        elif choice == "4":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        print()

if __name__ == "__main__":
    main()
