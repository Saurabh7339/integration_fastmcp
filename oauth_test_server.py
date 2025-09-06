#!/usr/bin/env python3
"""
Simple HTTP server for testing OAuth flow with MCP servers.
This provides a web interface to test the OAuth flow for Google services.
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from uuid import uuid4
from database import get_db_session, create_tables
from config import Config

# Import servers
from gdocs_server import GoogleDocsMCPServer
from gmail_server import GmailMCPServer
from gdrive_server import GoogleDriveMCPServer

class OAuthTestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.session = get_db_session()
        self.docs_server = GoogleDocsMCPServer(self.session)
        self.gmail_server = GmailMCPServer(self.session)
        self.drive_server = GoogleDriveMCPServer(self.session)
        self.test_workspace_id = self._get_or_create_test_workspace()
        super().__init__(*args, **kwargs)
    
    def _get_or_create_test_workspace(self):
        """Get or create a test workspace"""
        try:
            from database import get_or_create_workspace
            workspace = get_or_create_workspace("BIAgent-Workspace")
            print("printing the workspace",workspace)
            return workspace["id"]
        except Exception as e:
            print(f"Warning: Could not create workspace, using random UUID: {e}")
            return str(uuid4())
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == "/":
            self.serve_home_page()
        elif path == "/oauth":
            self.handle_oauth_request(parsed_path)
        elif path == "/google/callback":
            self.handle_oauth_callback(parsed_path)
        elif path == "/test":
            self.handle_test_request(parsed_path)
        else:
            self.send_error(404, "Not Found")
    
    def serve_home_page(self):
        """Serve the home page"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MCP OAuth Test</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .service { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                .service h3 { margin-top: 0; }
                .btn { background: #4285f4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 3px; display: inline-block; margin: 5px; }
                .btn:hover { background: #3367d6; }
                .result { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 3px; }
                .error { background: #ffebee; color: #c62828; }
                .success { background: #e8f5e8; color: #2e7d32; }
            </style>
        </head>
        <body>
            <h1>MCP Server OAuth Test</h1>
            <p>Test the OAuth flow for Google Docs, Gmail, and Google Drive MCP servers.</p>
            
            <div class="service">
                <h3>Google Docs</h3>
                <a href="/oauth?service=docs" class="btn">Get OAuth URL</a>
                <a href="/test?service=docs&action=status" class="btn">Check Status</a>
                <a href="/test?service=docs&action=tools" class="btn">Test Tools</a>
                <a href="/test?service=docs&action=clear" class="btn">Clear Credentials</a>
            </div>
            
            <div class="service">
                <h3>Gmail</h3>
                <a href="/oauth?service=gmail" class="btn">Get OAuth URL</a>
                <a href="/test?service=gmail&action=status" class="btn">Check Status</a>
                <a href="/test?service=gmail&action=tools" class="btn">Test Tools</a>
                <a href="/test?service=gmail&action=clear" class="btn">Clear Credentials</a>
            </div>
            
            <div class="service">
                <h3>Google Drive</h3>
                <a href="/oauth?service=drive" class="btn">Get OAuth URL</a>
                <a href="/test?service=drive&action=status" class="btn">Check Status</a>
                <a href="/test?service=drive&action=tools" class="btn">Test Tools</a>
                <a href="/test?service=drive&action=clear" class="btn">Clear Credentials</a>
            </div>
            
            <div class="service">
                <h3>OAuth Callback</h3>
                <p>After authorizing, you'll be redirected to: <code>http://localhost:8000/google/callback</code></p>
                <p>Copy the authorization code from the URL and use it to test the OAuth flow.</p>
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_oauth_request(self, parsed_path):
        """Handle OAuth URL requests"""
        query_params = parse_qs(parsed_path.query)
        service = query_params.get("service", [None])[0]
        
        if not service or service not in ["docs", "gmail", "drive"]:
            self.send_error(400, "Invalid service")
            return
        
        try:
            if service == "docs":
                url = self.docs_server.call_tool("get_docs_auth_url")
            elif service == "gmail":
                url = self.gmail_server.call_tool("get_gmail_auth_url")
            elif service == "drive":
                url = self.drive_server.call_tool("get_drive_auth_url")
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>OAuth URL - {service.upper()}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .url {{ background: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 3px; word-break: break-all; }}
                    .btn {{ background: #4285f4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 3px; display: inline-block; margin: 5px; }}
                </style>
            </head>
            <body>
                <h1>OAuth URL for {service.upper()}</h1>
                <div class="url">{url}</div>
                <a href="{url}" class="btn" target="_blank">Authorize {service.upper()}</a>
                <a href="/" class="btn">Back to Home</a>
            </body>
            </html>
            """
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
            
        except Exception as e:
            self.send_error(500, f"Error generating OAuth URL: {str(e)}")
    
    def handle_oauth_callback(self, parsed_path):
        """Handle OAuth callback"""
        query_params = parse_qs(parsed_path.query)
        code = query_params.get("code", [None])[0]
        error = query_params.get("error", [None])[0]
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>OAuth Callback</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .code { background: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 3px; word-break: break-all; }
                .btn { background: #4285f4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 3px; display: inline-block; margin: 5px; }
            </style>
        </head>
        <body>
            <h1>OAuth Callback</h1>
        """
        
        if error:
            html += f'<p class="error">Error: {error}</p>'
        elif code:
            html += f"""
            <p>Authorization code received:</p>
            <div class="code">{code}</div>
            <p>You can now use this code to test the OAuth flow.</p>
            """
        else:
            html += '<p>No authorization code received.</p>'
        
        html += '<a href="/" class="btn">Back to Home</a></body></html>'
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_test_request(self, parsed_path):
        """Handle test requests"""
        query_params = parse_qs(parsed_path.query)
        service = query_params.get("service", [None])[0]
        action = query_params.get("action", [None])[0]
        
        if not service or service not in ["docs", "gmail", "drive"]:
            self.send_error(400, "Invalid service")
            return
        
        if not action or action not in ["status", "tools", "clear"]:
            self.send_error(400, "Invalid action")
            return
        
        try:
            if action == "status":
                if service == "docs":
                    result = self.docs_server.call_tool("get_docs_credentials_status", self.test_workspace_id)
                elif service == "gmail":
                    result = self.gmail_server.call_tool("get_gmail_credentials_status", self.test_workspace_id)
                elif service == "drive":
                    result = self.drive_server.call_tool("get_drive_credentials_status", self.test_workspace_id)
            
            elif action == "tools":
                if service == "docs":
                    result = self.docs_server.call_tool("list_google_docs", self.test_workspace_id)
                elif service == "gmail":
                    result = self.gmail_server.call_tool("read_inbox", self.test_workspace_id)
                elif service == "drive":
                    result = self.drive_server.call_tool("list_drive_files", self.test_workspace_id)
            
            elif action == "clear":
                if service == "docs":
                    result = self.docs_server.call_tool("clear_google_credentials", self.test_workspace_id)
                elif service == "gmail":
                    result = self.gmail_server.call_tool("clear_google_credentials", self.test_workspace_id)
                elif service == "drive":
                    result = self.drive_server.call_tool("clear_google_credentials", self.test_workspace_id)
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Test Result - {service.upper()}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .result {{ background: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 3px; }}
                    .btn {{ background: #4285f4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 3px; display: inline-block; margin: 5px; }}
                </style>
            </head>
            <body>
                <h1>Test Result - {service.upper()} - {action.upper()}</h1>
                <div class="result">
                    <pre>{json.dumps(result, indent=2)}</pre>
                </div>
                <a href="/" class="btn">Back to Home</a>
            </body>
            </html>
            """
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
            
        except Exception as e:
            self.send_error(500, f"Error testing {service}: {str(e)}")
    
    def log_message(self, format, *args):
        """Override to reduce log noise"""
        pass

def main():
    """Main function"""
    print("Starting MCP OAuth Test Server")
    print("=" * 35)
    
    # Check environment
    print("Checking environment configuration...")
    required_vars = ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"✗ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before running the test server.")
        return
    
    print("✓ Environment configuration OK")
    
    # Create database tables
    try:
        create_tables()
        print("✓ Database tables created/verified")
    except Exception as e:
        print(f"✗ Error setting up database: {e}")
        return
    
    # Start server
    port = 8080
    server = HTTPServer(("localhost", port), OAuthTestHandler)
    
    print(f"✓ Server starting on http://localhost:{port}")
    print("Open your browser and navigate to the URL above to test OAuth flow")
    print("Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()

if __name__ == "__main__":
    main()
