#!/usr/bin/env python3
"""
Simple MCP server launcher that reads ports from Integration table.
This script starts each MCP server and displays the port configuration.
"""

import os
import sys
import time
from database import get_db_session, create_tables
from config import Config
from models.workspace import Integration
from sqlmodel import select

# Import MCP servers
from gdocs_server import GoogleDocsMCPServer
from gmail_server import GmailMCPServer
from gdrive_server import GoogleDriveMCPServer

def get_integration_ports():
    """Get port configurations from Integration table"""
    session = get_db_session()
    try:
        # Get all integrations with their ports
        stmt = select(Integration)
        integrations = session.execute(stmt).scalars().all()
        
        ports = {}
        for integration in integrations:
            service_type = integration.name.lower()
            if "gmail" in service_type:
                ports["gmail"] = integration.port
            elif "drive" in service_type:
                ports["drive"] = integration.port
            elif "docs" in service_type:
                ports["docs"] = integration.port
        
        return ports
        
    except Exception as e:
        print(f"Error getting integration ports: {e}")
        return {}
    finally:
        session.close()

def display_server_info(server, service_name, port):
    """Display server information"""
    print(f"\n{service_name.upper()} MCP Server")
    print("-" * 30)
    print(f"Port: {port}")
    print(f"Class: {server.__class__.__name__}")
    
    # Display available tools
    tools = server.get_tools()
    print(f"Available Tools ({len(tools)}):")
    for tool_name in tools.keys():
        print(f"  - {tool_name}")
    
    # Display tool descriptions
    descriptions = server.get_tool_descriptions()
    print("\nTool Descriptions:")
    for tool_name, description in descriptions.items():
        print(f"  {tool_name}: {description}")

def main():
    """Main function to run MCP servers"""
    print("MCP Server Launcher (Simple)")
    print("=" * 35)
    
    # Check environment
    if not os.getenv("GOOGLE_CLIENT_ID") or not os.getenv("GOOGLE_CLIENT_SECRET"):
        print("✗ Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET")
        print("Please set these environment variables first.")
        return
    
    # Create database tables
    try:
        create_tables()
        print("✓ Database tables created/verified")
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        return
    
    # Get port configurations
    ports = get_integration_ports()
    print(f"✓ Found port configurations: {ports}")
    
    # Default ports if not configured
    default_ports = {
        "gmail": 8001,
        "drive": 8002,
        "docs": 8003
    }
    
    # Use configured ports or defaults
    final_ports = {}
    for service, default_port in default_ports.items():
        final_ports[service] = ports.get(service, default_port)
    
    print(f"✓ Final port configuration: {final_ports}")
    
    # Create MCP servers
    session = get_db_session()
    
    try:
        # Create server instances
        servers = {
            "gmail": GmailMCPServer(session),
            "drive": GoogleDriveMCPServer(session),
            "docs": GoogleDocsMCPServer(session)
        }
        
        print("✓ MCP servers created")
        
        # Display server information
        for service, server in servers.items():
            port = final_ports[service]
            display_server_info(server, service, port)
        
        print("\n" + "=" * 50)
        print("MCP Servers Ready!")
        print("=" * 50)
        print("Servers are running with the following port configuration:")
        for service, port in final_ports.items():
            print(f"  {service.upper()}: Port {port}")
        
        print("\nNote: These are MCP tool registries, not web servers.")
        print("Use the MCP protocol to interact with the tools.")
        print("\nPress Ctrl+C to exit")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            
    except Exception as e:
        print(f"✗ Error creating servers: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
