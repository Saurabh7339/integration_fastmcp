#!/bin/bash

# MCP Servers Launcher Script
# This script runs all MCP servers for Google Services integration

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🚀 MCP Servers Launcher${NC}"
echo "=================================="

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "info")
            echo -e "${BLUE}ℹ️  $message${NC}"
            ;;
        "success")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "warning")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
        "error")
            echo -e "${RED}❌ $message${NC}"
            ;;
    esac
}

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    print_status "error" "Python3 is not installed or not in PATH"
    exit 1
fi

print_status "success" "Python3 found: $(python3 --version)"

# Check if required Python packages are installed
print_status "info" "Checking Python dependencies..."

required_packages=("fastapi" "uvicorn" "sqlmodel" "psycopg2" "google-auth" "google-auth-oauthlib" "google-auth-httplib2")

for package in "${required_packages[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        print_status "warning" "Package '$package' not found. Installing..."
        pip3 install "$package" || {
            print_status "error" "Failed to install package '$package'"
            exit 1
        }
    else
        print_status "success" "Package '$package' is available"
    fi
done

# Check environment variables
print_status "info" "Checking environment variables..."

# Check for Google OAuth credentials
if [[ -z "$GOOGLE_CLIENT_ID" && -z "$GMAIL_CLIENT_ID" && -z "$GDRIVE_CLIENT_ID" && -z "$GDOCS_CLIENT_ID" ]]; then
    print_status "error" "No Google OAuth credentials found!"
    print_status "info" "Please set at least one of the following:"
    echo "  - GOOGLE_CLIENT_ID (fallback for all services)"
    echo "  - GMAIL_CLIENT_ID (for Gmail service)"
    echo "  - GDRIVE_CLIENT_ID (for Google Drive service)"
    echo "  - GDOCS_CLIENT_ID (for Google Docs service)"
    echo ""
    print_status "info" "And their corresponding CLIENT_SECRET variables"
    exit 1
fi

if [[ -z "$GOOGLE_CLIENT_SECRET" && -z "$GMAIL_CLIENT_SECRET" && -z "$GDRIVE_CLIENT_SECRET" && -z "$GDOCS_CLIENT_SECRET" ]]; then
    print_status "error" "No Google OAuth client secrets found!"
    print_status "info" "Please set at least one of the following:"
    echo "  - GOOGLE_CLIENT_SECRET (fallback for all services)"
    echo "  - GMAIL_CLIENT_SECRET (for Gmail service)"
    echo "  - GDRIVE_CLIENT_SECRET (for Google Drive service)"
    echo "  - GDOCS_CLIENT_SECRET (for Google Docs service)"
    exit 1
fi

print_status "success" "OAuth credentials found"

# Check database connection
print_status "info" "Checking database connection..."

# Set default database URL if not provided
if [[ -z "$DATABASE_URL" ]]; then
    export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5433/oneplace_core"
    print_status "info" "Using default database URL: $DATABASE_URL"
fi

# Test database connection
if ! python3 -c "
import sys
sys.path.append('.')
from database import get_db_session
try:
    session = get_db_session()
    session.close()
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
    sys.exit(1)
" 2>/dev/null; then
    print_status "error" "Database connection failed!"
    print_status "info" "Please ensure PostgreSQL is running and accessible"
    print_status "info" "Default connection: postgresql+psycopg2://postgres:postgres@localhost:5433/oneplace_core"
    exit 1
fi

print_status "success" "Database connection successful"

# Check if .env file exists and load it
if [[ -f ".env" ]]; then
    print_status "info" "Loading environment variables from .env file"
    export $(grep -v '^#' .env | xargs)
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Function to cleanup on exit
cleanup() {
    print_status "info" "Shutting down MCP servers..."
    # Kill all background processes
    jobs -p | xargs -r kill
    print_status "success" "All servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the MCP servers
print_status "info" "Starting MCP servers..."

# Run the Python script in the background and capture its output
python3 run_mcp_servers.py > logs/mcp_servers.log 2>&1 &
MCP_PID=$!

# Wait a moment for servers to start
sleep 3

# Check if the process is still running
if ! kill -0 $MCP_PID 2>/dev/null; then
    print_status "error" "Failed to start MCP servers"
    print_status "info" "Check logs/mcp_servers.log for details"
    exit 1
fi

print_status "success" "MCP servers started successfully (PID: $MCP_PID)"

# Display server information
echo ""
echo "=================================="
echo -e "${GREEN}🎉 All MCP Servers Running!${NC}"
echo "=================================="
echo ""
echo -e "${BLUE}Server URLs:${NC}"
echo "  📧 Gmail Server:  http://localhost:8001"
echo "  📁 Drive Server:  http://localhost:8002"
echo "  📄 Docs Server:   http://localhost:8003"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo "  📋 Server logs: logs/mcp_servers.log"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""

# Monitor the process and display logs in real-time
tail -f logs/mcp_servers.log &
TAIL_PID=$!

# Wait for the MCP process to finish
wait $MCP_PID

# Clean up
kill $TAIL_PID 2>/dev/null || true
cleanup
