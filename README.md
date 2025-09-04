# 🚀 Google Services MCP Server

A powerful **Model Context Protocol (MCP)** server that provides seamless access to Google services (Gmail, Google Drive, and Google Docs) through OAuth authentication. This server enables LLMs and applications to interact with Google APIs using a standardized interface.

## ✨ Features

### 📧 Gmail Integration
- **Read Inbox**: Access and read emails with filtering and search
- **Send Emails**: Create and send emails with CC/BCC support
- **Check Sent**: View sent email history
- **Check Drafts**: Access draft emails
- **Check Promotions**: Filter promotional emails
- **Check Important**: Access important emails
- **Search Emails**: Advanced email search with Gmail query syntax

### 📁 Google Drive Integration
- **List Files**: Browse files and folders with pagination
- **Upload Files**: Upload files with automatic MIME type detection
- **Download Files**: Download files to local storage
- **Create Folders**: Organize files in folders
- **Share Files**: Control file access permissions
- **Search Files**: Find files using Drive search syntax
- **Move Files**: Reorganize file structure
- **Manage Permissions**: View and control file access

### 📝 Google Docs Integration
- **Create Documents**: Generate new documents with content
- **Read Documents**: Access document content and metadata
- **Update Documents**: Modify existing documents
- **List Documents**: Browse all available documents
- **Search Documents**: Find documents by content or title
- **Share Documents**: Control document access
- **Export Documents**: Convert to PDF, DOCX, TXT, or HTML
- **Add Comments**: Collaborate with comments

### 🔒 Security Features
- **OAuth 2.0 Authentication**: Industry-standard Google OAuth flow
- **Automatic Token Refresh**: Seamless credential management
- **User Isolation**: Separate credentials per user
- **Secure Storage**: Local credential storage with encryption support

## 🏗️ Architecture

### Separate MCP Servers Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   LLM/Client   │◄──►│  Gmail MCP       │◄──►│   Gmail API     │
│                 │    │   Server         │    │                 │
│ • FastMCP      │    │ • Authentication │    │ • Email         │
│ • HTTP Client  │    │ • Gmail Tools    │    │ • Labels        │
│ • Web UI       │    │ • Tool Registry  │    │ • Search        │
└─────────────────┘    └──────────────────┘    └─────────────────┘

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   LLM/Client   │◄──►│  Drive MCP       │◄──►│  Google Drive   │
│                 │    │   Server         │    │     API         │
│ • FastMCP      │    │ • Authentication │    │ • Files         │
│ • HTTP Client  │    │ • Drive Tools    │    │ • Folders       │
│ • Web UI       │    │ • Tool Registry  │    │ • Sharing       │
└─────────────────┘    └──────────────────┘    └─────────────────┘

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   LLM/Client   │◄──►│  Docs MCP        │◄──►│  Google Docs    │
│                 │    │   Server         │    │     API         │
│ • FastMCP      │    │ • Authentication │    │ • Documents     │
│ • HTTP Client  │    │ • Docs Tools     │    │ • Content       │
│ • Web UI       │    │ • Tool Registry  │    │ • Collaboration │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Benefits of Separate Servers

- **🔄 Independent Scaling**: Each service can scale independently based on demand
- **🔧 Service-Specific Config**: Custom configurations for each Google service
- **📦 Resource Isolation**: Better resource management and isolation
- **🛠️ Easier Maintenance**: Update and maintain each service separately
- **🌐 Distributed Deployment**: Run servers on different machines if needed
- **🎯 Selective Connection**: LLMs can connect only to the services they need

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Google Cloud Project with APIs enabled
- OAuth 2.0 credentials

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd fast_mcp

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp env.example .env
```

### 3. Google OAuth Setup

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable APIs**:
   - Gmail API
   - Google Drive API
   - Google Docs API

3. **Create OAuth Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Add redirect URI: `http://localhost:8000/auth/callback`

4. **Update Environment Variables**:
   ```bash
   # Edit .env file
   GOOGLE_CLIENT_ID=your_client_id_here
   GOOGLE_CLIENT_SECRET=your_client_secret_here
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
   ```

### 4. Run the Servers

#### Option 1: Separate Servers (Recommended)
```bash
# Use the startup script for easy management
./start_servers.sh

# Or start individual servers manually
python3 gmail_server.py      # Gmail MCP server
python3 gdrive_server.py     # Google Drive MCP server  
python3 gdocs_server.py      # Google Docs MCP server
```

#### Option 2: Combined Server (Legacy)
```bash
# Start the combined MCP server
python server.py

# Or start the web interface
python web_interface.py
```

#### Option 3: All Servers Simultaneously
```bash
# Start all three servers in separate terminals
./start_servers.sh
# Choose option 4 to start all servers
```

## 🧪 Testing

### Web Interface Testing

1. **Start the web interface**:
   ```bash
   python web_interface.py
   ```

2. **Open browser**: Navigate to `http://localhost:8000`

3. **Complete OAuth flow**:
   - Click "Start OAuth Authentication"
   - Authorize the application
   - Test the tools

### MCP Client Testing

#### Separate Servers Testing
```bash
# Test the separate servers
python3 test_separate_servers.py

# Or test individual servers
python3 test_client.py  # For combined server
```

#### Server Namespaces
- **Gmail Server**: `gmail-mcp-server`
- **Google Drive Server**: `gdrive-mcp-server`  
- **Google Docs Server**: `gdocs-mcp-server`

### Direct API Testing

#### Separate Servers
```python
from fastmcp import FastMCPClient

async def test_separate_servers():
    # Test Gmail server
    gmail_client = FastMCPClient("gmail-mcp-server")
    auth_url = await gmail_client.get_auth_url()
    print(f"Gmail Auth URL: {auth_url}")
    await gmail_client.close()
    
    # Test Drive server
    drive_client = FastMCPClient("gdrive-mcp-server")
    auth_url = await drive_client.get_auth_url()
    print(f"Drive Auth URL: {auth_url}")
    await drive_client.close()
    
    # Test Docs server
    docs_client = FastMCPClient("gdocs-mcp-server")
    auth_url = await docs_client.get_auth_url()
    print(f"Docs Auth URL: {auth_url}")
    await docs_client.close()

# Run the test
import asyncio
asyncio.run(test_separate_servers())
```

#### Combined Server (Legacy)
```python
from fastmcp import FastMCPClient

async def test_combined_server():
    client = FastMCPClient("google-services-mcp")
    
    # Test authentication
    auth_url = await client.get_auth_url()
    print(f"Auth URL: {auth_url}")
    
    # Test Gmail tools
    inbox = await client.read_inbox(max_results=5)
    print(f"Inbox: {inbox}")
    
    await client.close()

# Run the test
import asyncio
asyncio.run(test_combined_server())
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | Required |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | Required |
| `GOOGLE_REDIRECT_URI` | OAuth redirect URI | `http://localhost:8000/auth/callback` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `SECRET_KEY` | Application secret key | Auto-generated |

### OAuth Scopes

The application requests the following scopes:
- **Gmail**: `https://www.googleapis.com/auth/gmail.modify`
- **Drive**: `https://www.googleapis.com/auth/drive`
- **Docs**: `https://www.googleapis.com/auth/documents`

## 🚀 Separate Server Architecture

### Overview

The system now supports **three separate MCP servers**, each dedicated to a specific Google service:

1. **📧 Gmail MCP Server** (`gmail-mcp-server`)
2. **📁 Google Drive MCP Server** (`gdrive-mcp-server`)  
3. **📝 Google Docs MCP Server** (`gdocs-mcp-server`)

### Server Management

#### Starting Individual Servers
```bash
# Gmail server
python3 gmail_server.py

# Google Drive server  
python3 gdrive_server.py

# Google Docs server
python3 gdocs_server.py
```

#### Starting All Servers
```bash
# Use the startup script
./start_servers.sh
# Choose option 4 to start all servers simultaneously
```

#### Testing Separate Servers
```bash
# Test all servers
python3 test_separate_servers.py

# Or test individual servers
python3 test_client.py  # For combined server
```

### Server Namespaces

Each server has its own MCP namespace, allowing LLMs to connect independently:

- **Gmail**: `gmail-mcp-server` - Email operations
- **Drive**: `gdrive-mcp-server` - File management  
- **Docs**: `gdocs-mcp-server` - Document operations

### Architecture Comparison

| Feature | Combined Server | Separate Servers |
|---------|----------------|------------------|
| **Deployment** | Single process | Multiple processes |
| **Scaling** | All-or-nothing | Independent scaling |
| **Resource Usage** | Shared resources | Isolated resources |
| **Maintenance** | Single update | Service-specific updates |
| **LLM Connection** | All services | Selective services |
| **Fault Tolerance** | Single point of failure | Isolated failures |
| **Configuration** | Unified config | Service-specific config |

### Benefits

- **🔄 Independent Scaling**: Scale each service based on demand
- **🔧 Service-Specific Config**: Custom settings per service
- **📦 Resource Isolation**: Better resource management
- **🛠️ Easier Maintenance**: Update services independently
- **🌐 Distributed Deployment**: Run on different machines
- **🎯 Selective Connection**: LLMs choose needed services

## 📚 API Reference

### Authentication Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_auth_url` | Get OAuth authorization URL | None |
| `authenticate_user` | Exchange auth code for tokens | `authorization_code` |
| `get_user_credentials` | Check user credentials status | `user_id` (optional) |

### Gmail Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `read_inbox` | Read inbox emails | `user_id`, `max_results`, `query` |
| `create_email` | Send email | `user_id`, `to`, `subject`, `body`, `cc`, `bcc` |
| `check_sent_emails` | View sent emails | `user_id`, `max_results` |
| `check_drafts` | View draft emails | `user_id`, `max_results` |
| `check_promotions` | View promotional emails | `user_id`, `max_results` |
| `check_important_emails` | View important emails | `user_id`, `max_results` |
| `search_emails` | Search emails | `user_id`, `query`, `max_results` |

### Google Drive Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_drive_files` | List Drive files | `user_id`, `page_size`, `query` |
| `create_drive_folder` | Create folder | `user_id`, `name`, `parent_id` |
| `upload_drive_file` | Upload file | `user_id`, `file_path`, `name`, `parent_id` |
| `download_drive_file` | Download file | `user_id`, `file_id`, `destination_path` |
| `share_drive_file` | Share file | `user_id`, `file_id`, `email`, `role` |
| `search_drive_files` | Search files | `user_id`, `query`, `page_size` |

### Google Docs Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_google_doc` | Create document | `user_id`, `title`, `content` |
| `get_google_doc` | Read document | `user_id`, `document_id` |
| `update_google_doc` | Update document | `user_id`, `document_id`, `content`, `append` |
| `list_google_docs` | List documents | `user_id`, `page_size` |
| `search_google_docs` | Search documents | `user_id`, `query`, `page_size` |
| `share_google_doc` | Share document | `user_id`, `document_id`, `email`, `role` |
| `export_google_doc` | Export document | `user_id`, `document_id`, `export_format`, `output_path` |

## 🔐 Security Considerations

- **OAuth Flow**: Uses standard OAuth 2.0 with PKCE
- **Token Storage**: Credentials stored locally in `credentials/` directory
- **Scope Limitation**: Requests minimal necessary permissions
- **User Isolation**: Separate credentials per user ID
- **HTTPS**: Production deployments should use HTTPS

## 🚀 Production Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "server.py"]
```

### Environment Setup

```bash
# Production environment variables
GOOGLE_CLIENT_ID=your_production_client_id
GOOGLE_CLIENT_SECRET=your_production_client_secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/auth/callback
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your_secure_secret_key
```

### Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Create an issue on GitHub
- **Documentation**: Check this README and inline code comments
- **Community**: Join our discussions and contribute

## 🔗 Related Links

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Google APIs Documentation](https://developers.google.com/)
- [FastMCP Framework](https://github.com/fastmcp/fastmcp)
- [OAuth 2.0 Specification](https://oauth.net/2/)

---

**Made with ❤️ for the MCP community**
# mcp_external_services
