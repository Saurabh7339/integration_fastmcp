#!/usr/bin/env python3
"""
Demo script for the Separate Google Services MCP Servers
This script demonstrates the architecture and capabilities of the three separate servers.
"""

import os
import sys
import subprocess
import time

def print_header():
    """Print a beautiful header"""
    print("🚀 Google Services MCP - Separate Servers Demo")
    print("=" * 60)
    print()

def show_architecture():
    """Show the separate servers architecture"""
    print("🏗️  Architecture Overview")
    print("-" * 30)
    print()
    print("┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐")
    print("│   LLM/Client   │◄──►│  Gmail MCP       │◄──►│   Gmail API     │")
    print("│                 │    │   Server         │    │                 │")
    print("│ • FastMCP      │    │ • Authentication │    │ • Email         │")
    print("│ • HTTP Client  │    │ • Gmail Tools    │    │ • Labels        │")
    print("│ • Web UI       │    │ • Tool Registry  │    │ • Search        │")
    print("└─────────────────┘    └──────────────────┘    └─────────────────┘")
    print()
    print("┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐")
    print("│   LLM/Client   │◄──►│  Drive MCP       │◄──►│  Google Drive   │")
    print("│                 │    │   Server         │    │     API         │")
    print("│ • FastMCP      │    │ • Authentication │    │ • Files         │")
    print("│ • HTTP Client  │    │ • Drive Tools    │    │ • Folders       │")
    print("│ • Web UI       │    │ • Tool Registry  │    │ • Sharing       │")
    print("└─────────────────┘    └──────────────────┘    └─────────────────┘")
    print()
    print("┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐")
    print("│   LLM/Client   │◄──►│  Docs MCP        │◄──►│  Google Docs    │")
    print("│                 │    │   Server         │    │     API         │")
    print("│ • FastMCP      │    │ • Authentication │    │ • Documents     │")
    print("│ • HTTP Client  │    │ • Docs Tools     │    │ • Content       │")
    print("│ • Web UI       │    │ • Tool Registry  │    │ • Collaboration │")
    print("└─────────────────┘    └──────────────────┘    └─────────────────┘")
    print()

def show_server_details():
    """Show details about each server"""
    print("📋 Server Details")
    print("-" * 30)
    print()
    
    print("📧 Gmail MCP Server (gmail-mcp-server)")
    print("   Namespace: gmail-mcp-server")
    print("   File: gmail_server.py")
    print("   Tools: 8 Gmail-specific tools + 3 authentication tools")
    print("   Features:")
    print("     • Read inbox, send emails")
    print("     • Check sent/drafts/promotions/important emails")
    print("     • Search emails with Gmail query syntax")
    print("     • Get email details")
    print()
    
    print("📁 Google Drive MCP Server (gdrive-mcp-server)")
    print("   Namespace: gdrive-mcp-server")
    print("   File: gdrive_server.py")
    print("   Tools: 11 Drive-specific tools + 3 authentication tools")
    print("   Features:")
    print("     • File upload/download/management")
    print("     • Folder creation and organization")
    print("     • File sharing and permissions")
    print("     • Search and move files")
    print("     • View shared and starred files")
    print()
    
    print("📝 Google Docs MCP Server (gdocs-mcp-server)")
    print("   Namespace: gdocs-mcp-server")
    print("   File: gdocs_server.py")
    print("   Tools: 12 Docs-specific tools + 3 authentication tools")
    print("   Features:")
    print("     • Document creation and editing")
    print("     • Content management and search")
    print("     • Document sharing and collaboration")
    print("     • Export to multiple formats")
    print("     • Comments and permissions")
    print()

def show_benefits():
    """Show benefits of separate servers"""
    print("🚀 Benefits of Separate Servers")
    print("-" * 30)
    print()
    print("✅ Independent Scaling")
    print("   Each service can scale based on its own demand")
    print()
    print("✅ Service-Specific Configuration")
    print("   Custom settings and optimizations per service")
    print()
    print("✅ Resource Isolation")
    print("   Better resource management and fault isolation")
    print()
    print("✅ Easier Maintenance")
    print("   Update and maintain each service independently")
    print()
    print("✅ Distributed Deployment")
    print("   Run servers on different machines if needed")
    print()
    print("✅ Selective Connection")
    print("   LLMs can connect only to the services they need")
    print()

def show_usage_examples():
    """Show usage examples"""
    print("💡 Usage Examples")
    print("-" * 30)
    print()
    
    print("🔧 Starting Individual Servers:")
    print("   python3 gmail_server.py")
    print("   python3 gdrive_server.py")
    print("   python3 gdocs_server.py")
    print()
    
    print("🚀 Starting All Servers:")
    print("   ./start_servers.sh")
    print("   # Choose option 4 to start all servers simultaneously")
    print()
    
    print("🧪 Testing Servers:")
    print("   python3 test_separate_servers.py")
    print("   python3 demo_servers.py")
    print()
    
    print("🌐 Web Interface:")
    print("   python3 web_interface.py")
    print("   # Open http://localhost:8000")
    print()

def show_llm_integration():
    """Show LLM integration examples"""
    print("🤖 LLM Integration")
    print("-" * 30)
    print()
    
    print("📧 For Email Operations:")
    print("   Connect to: gmail-mcp-server")
    print("   Use tools: read_inbox, create_email, search_emails")
    print()
    
    print("📁 For File Operations:")
    print("   Connect to: gdrive-mcp-server")
    print("   Use tools: list_drive_files, upload_drive_file, share_drive_file")
    print()
    
    print("📝 For Document Operations:")
    print("   Connect to: gdocs-mcp-server")
    print("   Use tools: create_google_doc, update_google_doc, export_google_doc")
    print()
    
    print("🔐 Authentication:")
    print("   Each server has its own OAuth flow")
    print("   Credentials are stored per user and service")
    print("   Automatic token refresh for seamless operation")
    print()

def check_servers_status():
    """Check if servers are running"""
    print("🔍 Server Status Check")
    print("-" * 30)
    print()
    
    servers = [
        ("Gmail Server", "gmail_server.py"),
        ("Google Drive Server", "gdrive_server.py"),
        ("Google Docs Server", "gdocs_server.py")
    ]
    
    for name, file in servers:
        try:
            result = subprocess.run(
                ["pgrep", "-f", file],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ {name}: Running")
            else:
                print(f"❌ {name}: Not running")
        except Exception:
            print(f"❓ {name}: Status unknown")
    
    print()

def main():
    """Main demo function"""
    print_header()
    
    while True:
        print("Choose an option:")
        print("1) 🏗️  Show Architecture")
        print("2) 📋 Show Server Details")
        print("3) 🚀 Show Benefits")
        print("4) 💡 Show Usage Examples")
        print("5) 🤖 Show LLM Integration")
        print("6) 🔍 Check Server Status")
        print("7) 🚪 Exit")
        print()
        
        choice = input("Enter your choice (1-7): ").strip()
        print()
        
        if choice == "1":
            show_architecture()
        elif choice == "2":
            show_server_details()
        elif choice == "3":
            show_benefits()
        elif choice == "4":
            show_usage_examples()
        elif choice == "5":
            show_llm_integration()
        elif choice == "6":
            check_servers_status()
        elif choice == "7":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("Press Enter to continue...")
        print()

if __name__ == "__main__":
    main()
