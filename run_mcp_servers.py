#!/usr/bin/env python3
"""
Run MCP servers on ports specified in the Integration table.
This script reads the port configuration from the database and starts each MCP server on its designated port.
"""

import asyncio
import json
import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from database import get_db_session, create_tables
from config import Config
from models.workspace import Integration
from sqlmodel import select

# Import MCP servers
from gdocs_server import GoogleDocsMCPServer
from gmail_server import GmailMCPServer
from gdrive_server import GoogleDriveMCPServer

class MCPHandler(BaseHTTPRequestHandler):
    """HTTP handler for MCP server endpoints"""
    
    def __init__(self, mcp_server, *args, **kwargs):
        self.mcp_server = mcp_server
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == "/":
            self.serve_home_page()
        elif self.path == "/tools":
            self.serve_tools()
        elif self.path.startswith("/call/"):
            self.handle_tool_call()
        else:
            self.send_error(404, "Not Found")
    
    def serve_home_page(self):
        """Serve the home page"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MCP Server - {self.mcp_server.__class__.__name__}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .server-info {{ background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .tools {{ margin: 20px 0; }}
                .tool {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <h1>MCP Server: {self.mcp_server.__class__.__name__}</h1>
            <div class="server-info">
                <h3>Server Information</h3>
                <p><strong>Class:</strong> {self.mcp_server.__class__.__name__}</p>
                <p><strong>Port:</strong> {self.server.server_port}</p>
                <p><strong>Status:</strong> Running</p>
            </div>
            <div class="tools">
                <h3>Available Tools</h3>
                <a href="/tools">View All Tools</a>
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_tools(self):
        """Serve tools information"""
        tools = self.mcp_server.get_tools()
        descriptions = self.mcp_server.get_tool_descriptions()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MCP Tools - {self.mcp_server.__class__.__name__}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .tool {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                .tool-name {{ font-weight: bold; color: #4285f4; }}
                .tool-desc {{ margin: 10px 0; color: #666; }}
            </style>
        </head>
        <body>
            <h1>Available Tools</h1>
            <a href="/">← Back to Home</a>
        """
        
        for tool_name, tool_func in tools.items():
            description = descriptions.get(tool_name, "No description available")
            html += f"""
            <div class="tool">
                <div class="tool-name">{tool_name}</div>
                <div class="tool-desc">{description}</div>
            </div>
            """
        
        html += "</body></html>"
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_tool_call(self):
        """Handle tool calls"""
        # Extract tool name from path
        tool_name = self.path.split("/call/")[1]
        
        try:
            # For now, just return tool info
            result = {
                "tool": tool_name,
                "status": "available",
                "message": f"Tool {tool_name} is available for calling"
            }
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())
            
        except Exception as e:
            error_result = {
                "error": str(e),
                "tool": tool_name
            }
            
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(error_result, indent=2).encode())

def create_handler_class(mcp_server):
    """Create a handler class with the MCP server instance"""
    class Handler(MCPHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(mcp_server, *args, **kwargs)
    return Handler

def run_server_on_port(mcp_server, port, server_name):
    """Run an MCP server on a specific port"""
    try:
        handler_class = create_handler_class(mcp_server)
        server = HTTPServer(("localhost", port), handler_class)
        
        print(f"✓ {server_name} server starting on port {port}")
        print(f"  URL: http://localhost:{port}")
        print(f"  Tools: http://localhost:{port}/tools")
        
        server.serve_forever()
        
    except Exception as e:
        print(f"✗ Error starting {server_name} server on port {port}: {e}")

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

def main():
    """Main function to run MCP servers on configured ports"""
    print("MCP Server Launcher")
    print("=" * 20)
    
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
        
        # Start servers in separate threads
        threads = []
        for service, server in servers.items():
            port = final_ports[service]
            thread = threading.Thread(
                target=run_server_on_port,
                args=(server, port, service.upper()),
                daemon=True
            )
            thread.start()
            threads.append(thread)
            time.sleep(0.5)  # Small delay between server starts
        
        print("\n" + "=" * 50)
        print("All MCP Servers Started!")
        print("=" * 50)
        print(f"Gmail Server:  http://localhost:{final_ports['gmail']}")
        print(f"Drive Server:  http://localhost:{final_ports['drive']}")
        print(f"Docs Server:   http://localhost:{final_ports['docs']}")
        print("\nPress Ctrl+C to stop all servers")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down servers...")
            
    except Exception as e:
        print(f"✗ Error creating servers: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
