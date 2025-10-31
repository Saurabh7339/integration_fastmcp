# MCP Servers Launcher Scripts

This directory contains shell scripts to easily run all MCP (Model Context Protocol) servers for Google Services integration.

## Available Scripts

### 1. `run_mcp_servers.sh` (Comprehensive)
A full-featured launcher with dependency checking, environment validation, and logging.

**Features:**
- ✅ Dependency checking and auto-installation
- ✅ Environment variable validation
- ✅ Database connection testing
- ✅ Colored output and status messages
- ✅ Log file management
- ✅ Graceful shutdown handling
- ✅ Real-time log monitoring

### 2. `start_mcp.sh` (Simple)
A lightweight launcher for quick starts.

**Features:**
- ✅ Quick startup
- ✅ Environment file loading
- ✅ Basic logging

## Prerequisites

### Required Environment Variables

At minimum, you need to set one of these credential pairs:

```bash
# Option 1: Generic credentials (fallback for all services)
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"

# Option 2: Service-specific credentials (recommended)
export GMAIL_CLIENT_ID="your-gmail-client-id"
export GMAIL_CLIENT_SECRET="your-gmail-client-secret"

export GDRIVE_CLIENT_ID="your-drive-client-id"
export GDRIVE_CLIENT_SECRET="your-drive-client-secret"

export GDOCS_CLIENT_ID="your-docs-client-id"
export GDOCS_CLIENT_SECRET="your-docs-client-secret"
```

### Database Configuration

```bash
# Default PostgreSQL connection
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5433/oneplace_core"
```

### Optional Environment Variables

```bash
# Server configuration
export HOST="0.0.0.0"
export PORT="8000"

# OAuth redirect URI
export GOOGLE_REDIRECT_URI="http://localhost:8000/google/callback"

# API scopes (optional, defaults provided)
export GMAIL_SCOPE="https://www.googleapis.com/auth/gmail.modify"
export GDRIVE_SCOPE="https://www.googleapis.com/auth/drive"
export GDOCS_SCOPE="https://www.googleapis.com/auth/documents"
```

## Usage

### Method 1: Using the Comprehensive Script

```bash
# Make executable (first time only)
chmod +x run_mcp_servers.sh

# Run the servers
./run_mcp_servers.sh
```

### Method 2: Using the Simple Script

```bash
# Make executable (first time only)
chmod +x start_mcp.sh

# Run the servers
./start_mcp.sh
```

### Method 3: Direct Python Execution

```bash
# Run directly with Python
python3 run_mcp_servers.py
```

## What Gets Started

The scripts will start the following MCP servers:

| Service | Default Port | URL | Description |
|---------|-------------|-----|-------------|
| Gmail | 8001 | http://localhost:8001 | Gmail integration server |
| Google Drive | 8002 | http://localhost:8002 | Google Drive integration server |
| Google Docs | 8003 | http://localhost:8003 | Google Docs integration server |

## Server Features

Each MCP server provides:

- **Home Page**: Basic server information and status
- **Tools Endpoint**: List of available tools and their descriptions
- **Tool Calls**: HTTP endpoints for calling specific tools

### Example Server URLs

- Gmail Server Home: http://localhost:8001/
- Gmail Tools: http://localhost:8001/tools
- Drive Server Home: http://localhost:8002/
- Drive Tools: http://localhost:8002/tools
- Docs Server Home: http://localhost:8003/
- Docs Tools: http://localhost:8003/tools

## Logging

### Comprehensive Script (`run_mcp_servers.sh`)
- Logs are written to `logs/mcp_servers.log`
- Real-time log monitoring in terminal
- Colored output for better readability

### Simple Script (`start_mcp.sh`)
- Basic console output
- No persistent logging

## Environment File Support

Both scripts support loading environment variables from a `.env` file:

```bash
# Create .env file
cat > .env << EOF
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/oneplace_core
EOF
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   # Install required packages
   pip3 install fastapi uvicorn sqlmodel psycopg2 google-auth google-auth-oauthlib google-auth-httplib2
   ```

2. **Database Connection Issues**
   ```bash
   # Check if PostgreSQL is running
   sudo systemctl status postgresql
   
   # Test connection
   psql -h localhost -p 5433 -U postgres -d oneplace_core
   ```

3. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8001
   lsof -i :8002
   lsof -i :8003
   
   # Kill process if needed
   kill -9 <PID>
   ```

4. **OAuth Credentials Issues**
   - Ensure credentials are properly set in environment variables
   - Verify Google OAuth app configuration
   - Check redirect URI matches your setup

### Getting Help

1. Check the log files: `logs/mcp_servers.log`
2. Verify environment variables: `env | grep -E "(GOOGLE|DATABASE)"`
3. Test database connection manually
4. Check server status at the home URLs

## Stopping the Servers

- Press `Ctrl+C` in the terminal where the script is running
- The script will gracefully shut down all servers
- All background processes will be terminated

## Integration with Main API

These MCP servers work in conjunction with the main API server (`main.py`):

1. Start the MCP servers: `./run_mcp_servers.sh`
2. Start the main API: `python3 main.py`
3. Use the main API for OAuth flows and service management
4. MCP servers handle the actual Google API interactions

## Development

For development purposes, you can run individual servers:

```bash
# Run only Gmail server
python3 -c "
from gmail_server import GmailMCPServer
from database import get_db_session
import threading
from http.server import HTTPServer

session = get_db_session()
server = GmailMCPServer(session)
# ... server setup code
"
```

## Security Notes

- Never commit OAuth credentials to version control
- Use environment variables or secure credential management
- Ensure database connections use proper authentication
- Consider using HTTPS in production environments
