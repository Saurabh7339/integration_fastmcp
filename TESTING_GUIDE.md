# 🧪 Testing Guide for Separate MCP Servers

## Overview

This guide explains how to properly test the three separate MCP servers and addresses common testing issues.

## 🚨 Common Testing Issues

### Issue 1: `test_separate_servers.py` Connection Errors

**Problem**: The original test script shows errors like:
```
❌ Gmail server test failed: Could not infer a valid transport from: gmail-mcp-server
```

**Cause**: The FastMCP client library expects a different transport configuration than what our servers use.

**Solution**: Use the new testing scripts that properly communicate with the servers.

## ✅ Working Test Scripts

### 1. `test_server_connection.py` - Server Status Testing

This script tests the actual server processes and their startup/shutdown capabilities.

**Features**:
- ✅ Check which servers are currently running
- ✅ Test server startup and shutdown
- ✅ Verify server responsiveness
- ✅ Show server information and usage instructions

**Usage**:
```bash
python3 test_server_connection.py
```

**Example Output**:
```
🔍 Checking Running Servers
==================================================
✅ Gmail Server: Running (PIDs: 29779, 37477)
✅ Google Drive Server: Running (PIDs: 37475)
✅ Google Docs Server: Running (PIDs: 37473)

📊 Summary: 3 servers running
```

### 2. `mcp_client_example.py` - MCP Communication Testing

This script demonstrates proper MCP protocol communication with the servers.

**Features**:
- ✅ Test actual MCP protocol communication
- ✅ Initialize server connections
- ✅ Show connection guides
- ✅ List available tools

**Usage**:
```bash
python3 mcp_client_example.py
```

**Example Output**:
```
📧 Testing Gmail MCP Server
========================================
✅ Gmail server started
📊 Process ID: 42856

🔍 Testing MCP communication...
✅ MCP initialization successful
📋 Server info: {'name': 'gmail-mcp-server', 'version': '1.13.1'}
```

### 3. `demo_servers.py` - Architecture Demonstration

This script provides a comprehensive overview of the separate server architecture.

**Features**:
- ✅ Show architecture diagrams
- ✅ Display server details and benefits
- ✅ Provide usage examples
- ✅ Show LLM integration guides

**Usage**:
```bash
python3 demo_servers.py
```

## 🚀 Server Management

### Starting Servers

#### Option 1: Individual Servers
```bash
# Terminal 1
python3 gmail_server.py

# Terminal 2
python3 gdrive_server.py

# Terminal 3
python3 gdocs_server.py
```

#### Option 2: All Servers at Once
```bash
./start_servers.sh
# Choose option 4 to start all servers simultaneously
```

### Checking Server Status

```bash
# Check running processes
ps aux | grep -E "(gmail_server|gdrive_server|gdocs_server)" | grep -v grep

# Use the test script
python3 test_server_connection.py
# Choose option 1: Check Running Servers
```

## 🔧 Server Configuration

### Server Namespaces
- **Gmail Server**: `gmail-mcp-server`
- **Google Drive Server**: `gdrive-mcp-server`
- **Google Docs Server**: `gdocs-mcp-server`

### Transport Method
All servers use **STDIO transport** and communicate via stdin/stdout.

### Authentication
Each server has its own OAuth flow and credential storage.

## 🛠️ Available Tools by Server

### Gmail Server (8 tools + 3 auth)
- `read_inbox` - Read emails from inbox
- `create_email` - Send emails
- `check_sent_emails` - View sent emails
- `check_drafts` - View draft emails
- `check_promotions` - View promotional emails
- `check_important_emails` - View important emails
- `search_emails` - Search emails
- `get_email_details` - Get email details

### Google Drive Server (11 tools + 3 auth)
- `list_drive_files` - List files and folders
- `create_drive_folder` - Create new folders
- `upload_drive_file` - Upload files
- `download_drive_file` - Download files
- `share_drive_file` - Share files
- `search_drive_files` - Search for files
- `delete_drive_file` - Delete files
- `move_drive_file` - Move files
- `get_drive_file_info` - Get file details
- `get_shared_drive_files` - View shared files
- `get_starred_drive_files` - View starred files

### Google Docs Server (12 tools + 3 auth)
- `create_google_doc` - Create new documents
- `get_google_doc` - Read document content
- `update_google_doc` - Edit documents
- `list_google_docs` - Browse all documents
- `search_google_docs` - Find documents
- `share_google_doc` - Share documents
- `export_google_doc` - Export to different formats
- `add_comment_to_doc` - Add comments
- `delete_google_doc` - Remove documents
- `get_doc_permissions` - View access list
- `duplicate_google_doc` - Copy documents

## 🤖 LLM Integration

### Connecting to Servers

LLMs should connect to each server separately using the server namespaces:

```python
# For email operations
# Connect to: gmail-mcp-server
# Use tools: read_inbox, create_email, search_emails

# For file operations  
# Connect to: gdrive-mcp-server
# Use tools: list_drive_files, upload_drive_file, share_drive_file

# For document operations
# Connect to: gdocs-mcp-server
# Use tools: create_google_doc, update_google_doc, export_google_doc
```

### Authentication Flow

1. **Get Authorization URL**: `get_auth_url()`
2. **Complete OAuth**: `authenticate_user(authorization_code)`
3. **Check Credentials**: `get_user_credentials(user_id)`

## 🌐 Web Interface

For testing with a web interface:

```bash
python3 web_interface.py
# Open http://localhost:8000
```

The web interface provides:
- OAuth authentication flow
- Tool testing interface
- Real-time API testing

## 📋 Testing Checklist

### ✅ Server Startup Tests
- [ ] Gmail server starts successfully
- [ ] Google Drive server starts successfully  
- [ ] Google Docs server starts successfully
- [ ] All servers show proper startup messages
- [ ] Servers can be shut down cleanly

### ✅ Communication Tests
- [ ] MCP protocol initialization works
- [ ] Server responds to basic requests
- [ ] Authentication tools are available
- [ ] Service-specific tools are available

### ✅ Integration Tests
- [ ] OAuth flow works for each server
- [ ] Credentials are stored properly
- [ ] Tools can be called with valid credentials
- [ ] Error handling works for invalid requests

## 🔍 Troubleshooting

### Server Won't Start
1. Check Python environment: `python3 --version`
2. Verify dependencies: `pip3 list | grep fastmcp`
3. Check for port conflicts
4. Review error messages in terminal

### Connection Issues
1. Verify servers are running: `ps aux | grep server`
2. Check server namespaces match
3. Ensure proper transport method (STDIO)
4. Review MCP protocol compatibility

### Authentication Issues
1. Verify Google OAuth credentials in `.env`
2. Check redirect URI configuration
3. Ensure proper scopes are enabled
4. Review credential storage permissions

## 📚 Additional Resources

- **README.md**: Complete setup and usage guide
- **demo_servers.py**: Architecture demonstration
- **test_server_connection.py**: Server testing
- **mcp_client_example.py**: MCP communication examples
- **start_servers.sh**: Server management script

## 🎯 Summary

The separate MCP servers are working correctly. The original `test_separate_servers.py` had transport configuration issues, but the new testing scripts provide proper functionality for:

- ✅ Server status checking
- ✅ MCP communication testing  
- ✅ Architecture demonstration
- ✅ Usage guidance

Use the new testing scripts for reliable server testing and validation.
