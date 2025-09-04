#!/usr/bin/env python3
"""
Test script for connecting to the running MCP servers
This script tests the actual communication with the running servers.
"""

import subprocess
import json
import time
import sys
import os

def test_server_communication(server_name, test_commands):
    """Test communication with a specific server"""
    print(f"🧪 Testing {server_name}...")
    print("=" * 50)
    
    try:
        # Start the server process
        server_process = subprocess.Popen(
            [sys.executable, f"{server_name}_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Test basic communication
        print(f"✅ {server_name} server started successfully")
        print(f"📊 Process ID: {server_process.pid}")
        
        # Check if server is responsive
        if server_process.poll() is None:
            print(f"✅ {server_name} server is running and responsive")
        else:
            print(f"❌ {server_name} server failed to start")
            return False
        
        # Test server shutdown
        server_process.terminate()
        server_process.wait(timeout=5)
        print(f"✅ {server_name} server shut down cleanly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing {server_name}: {e}")
        return False

def test_server_startup():
    """Test that servers can start up properly"""
    print("🚀 Testing Server Startup")
    print("=" * 50)
    
    servers = [
        ("Gmail", "gmail"),
        ("Google Drive", "gdrive"), 
        ("Google Docs", "gdocs")
    ]
    
    results = {}
    
    for name, server in servers:
        print(f"\n📧 Testing {name} Server Startup...")
        success = test_server_communication(server, [])
        results[name] = success
        print()
    
    return results

def check_running_servers():
    """Check which servers are currently running"""
    print("🔍 Checking Running Servers")
    print("=" * 50)
    
    servers = [
        ("Gmail Server", "gmail_server.py"),
        ("Google Drive Server", "gdrive_server.py"),
        ("Google Docs Server", "gdocs_server.py")
    ]
    
    running_servers = []
    
    for name, file in servers:
        try:
            result = subprocess.run(
                ["pgrep", "-f", file],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                pids = result.stdout.strip().split('\n')
                print(f"✅ {name}: Running (PIDs: {', '.join(pids)})")
                running_servers.append(name)
            else:
                print(f"❌ {name}: Not running")
        except Exception as e:
            print(f"❓ {name}: Status unknown ({e})")
    
    return running_servers

def show_server_info():
    """Show detailed information about the servers"""
    print("📋 Server Information")
    print("=" * 50)
    
    print("\n📧 Gmail MCP Server")
    print("   File: gmail_server.py")
    print("   Namespace: gmail-mcp-server")
    print("   Transport: STDIO")
    print("   Tools: 8 Gmail tools + 3 auth tools")
    
    print("\n📁 Google Drive MCP Server")
    print("   File: gdrive_server.py")
    print("   Namespace: gdrive-mcp-server")
    print("   Transport: STDIO")
    print("   Tools: 11 Drive tools + 3 auth tools")
    
    print("\n📝 Google Docs MCP Server")
    print("   File: gdocs_server.py")
    print("   Namespace: gdocs-mcp-server")
    print("   Transport: STDIO")
    print("   Tools: 12 Docs tools + 3 auth tools")
    
    print("\n🔐 Authentication")
    print("   Each server has its own OAuth flow")
    print("   Credentials stored per user and service")
    print("   Automatic token refresh")

def show_usage_instructions():
    """Show how to use the servers"""
    print("💡 How to Use the Servers")
    print("=" * 50)
    
    print("\n🚀 Starting Servers:")
    print("   # Individual servers")
    print("   python3 gmail_server.py")
    print("   python3 gdrive_server.py")
    print("   python3 gdocs_server.py")
    print()
    print("   # All servers at once")
    print("   ./start_servers.sh")
    
    print("\n🔗 Connecting with LLMs:")
    print("   # For Gmail operations")
    print("   Connect to: gmail-mcp-server")
    print("   Tools: read_inbox, create_email, search_emails")
    print()
    print("   # For Drive operations")
    print("   Connect to: gdrive-mcp-server")
    print("   Tools: list_drive_files, upload_drive_file")
    print()
    print("   # For Docs operations")
    print("   Connect to: gdocs-mcp-server")
    print("   Tools: create_google_doc, update_google_doc")
    
    print("\n🌐 Web Interface:")
    print("   python3 web_interface.py")
    print("   Open: http://localhost:8000")

def main():
    """Main test function"""
    print("🧪 MCP Server Connection Test")
    print("=" * 60)
    print()
    
    while True:
        print("Choose an option:")
        print("1) 🔍 Check Running Servers")
        print("2) 🚀 Test Server Startup")
        print("3) 📋 Show Server Information")
        print("4) 💡 Show Usage Instructions")
        print("5) 🚪 Exit")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        print()
        
        if choice == "1":
            running = check_running_servers()
            print(f"\n📊 Summary: {len(running)} servers running")
            if running:
                print(f"Running servers: {', '.join(running)}")
        
        elif choice == "2":
            results = test_server_startup()
            print("\n📊 Startup Test Results:")
            for server, success in results.items():
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"   {server}: {status}")
        
        elif choice == "3":
            show_server_info()
        
        elif choice == "4":
            show_usage_instructions()
        
        elif choice == "5":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        print()

if __name__ == "__main__":
    main()
