#!/usr/bin/env python3
"""
Run MCP servers using FastMCP's built-in SSE transport.
This script reads the port configuration from the database and starts each MCP server using fastmcp run command.
"""

import os
import sys
import subprocess
import threading
import time
import signal
from database import get_db_session, create_tables
from config import Config
from models.workspace import Integration
from sqlmodel import select

# Global list to track running processes
running_processes = []

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
            port = integration.port
            
            # Debug output
            print(f"Found integration: {integration.name} -> port: {port}")
            
            # Only use valid ports (not None)
            if port is not None:
                if "gmail" in service_type:
                    ports["gmail"] = port
                elif "drive" in service_type:
                    ports["drive"] = port
                elif "docs" in service_type:
                    ports["docs"] = port
        
        return ports
        
    except Exception as e:
        print(f"Error getting integration ports: {e}")
        return {}
    finally:
        session.close()

def run_fastmcp_server(server_file, port, server_name):
    """Run a FastMCP server using the fastmcp run command with SSE transport"""
    try:
        # Construct the fastmcp run command
        cmd = [
            "fastmcp", "run", f"{server_file}:mcp",
            "--transport", "sse",
            "--port", str(port)
        ]
        
        print(f"✓ {server_name} server starting on port {port}")
        print(f"  Command: {' '.join(cmd)}")
        print(f"  SSE Endpoint: http://localhost:{port}/mcp/sse")
        
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Add to global list for cleanup
        running_processes.append(process)
        
        # Stream output in real-time
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[{server_name}] {line.strip()}")
        
        process.wait()
        
    except Exception as e:
        print(f"✗ Error starting {server_name} server on port {port}: {e}")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\nShutting down servers...")
    for process in running_processes:
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            print(f"Error stopping process: {e}")
    sys.exit(0)

def main():
    """Main function to run MCP servers using FastMCP SSE transport"""
    print("MCP Server Launcher (FastMCP SSE)")
    print("=" * 35)
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
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
        "gmail": 8030,
        "drive": 8031,
        "docs": 8032
    }
    
    # Use configured ports or defaults
    final_ports = {}
    for service, default_port in default_ports.items():
        final_ports[service] = ports.get(service, default_port)
    
    print(f"✓ Final port configuration: {final_ports}")
    
    # Server file mappings
    server_files = {
        "gmail": "gmail_server.py",
        "drive": "gdrive_server.py", 
        "docs": "gdocs_server.py"
    }
    
    # Start servers in separate threads
    threads = []
    for service, port in final_ports.items():
        # Validate port is not None
        if port is None:
            print(f"✗ Skipping {service} server - port is None")
            continue
            
        server_file = server_files[service]
        thread = threading.Thread(
            target=run_fastmcp_server,
            args=(server_file, port, service.upper()),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        time.sleep(1)  # Delay between server starts
    
    print("\n" + "=" * 50)
    print("All MCP Servers Started with SSE Transport!")
    print("=" * 50)
    
    # Display only servers that are actually running
    for service, port in final_ports.items():
        if port is not None:
            print(f"{service.upper()} Server:  http://localhost:{port}/mcp/sse")
    
    print("\nPress Ctrl+C to stop all servers")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()