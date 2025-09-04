#!/bin/bash

# Google Services MCP Server Startup Script

echo "🚀 Starting Google Services MCP Server..."
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if requirements are installed
if [ ! -d "venv" ] && [ ! -f ".env" ]; then
    echo "⚠️  First time setup detected..."
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    
    echo "📝 Setting up environment..."
    if [ ! -f ".env" ]; then
        cp env.example .env
        echo "✅ Environment file created. Please edit .env with your Google OAuth credentials."
        echo "🔑 You need to:"
        echo "   1. Create a Google Cloud Project"
        echo "   2. Enable Gmail, Drive, and Docs APIs"
        echo "   3. Create OAuth 2.0 credentials"
        echo "   4. Update GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env"
        echo ""
        echo "Press Enter when you're ready to continue..."
        read
    fi
fi

# Check if .env exists and has required values
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run setup first."
    exit 1
fi

# Load environment variables
source .env

# Check required environment variables
if [ -z "$GOOGLE_CLIENT_ID" ] || [ -z "$GOOGLE_CLIENT_SECRET" ]; then
    echo "❌ Missing required environment variables:"
    echo "   - GOOGLE_CLIENT_ID"
    echo "   - GOOGLE_CLIENT_SECRET"
    echo "Please update your .env file with these values."
    exit 1
fi

echo "✅ Environment configured successfully!"
echo ""

# Show menu
echo "Choose an option:"
echo "1) 🚀 Start MCP Server (for LLM integration)"
echo "2) 🌐 Start Web Interface (for testing)"
echo "3) 🧪 Run Test Client"
echo "4) 📚 Show Documentation"
echo "5) 🚪 Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🚀 Starting MCP Server..."
        echo "The server will be available for LLM connections."
        echo "Press Ctrl+C to stop the server."
        python3 server.py
        ;;
    2)
        echo "🌐 Starting Web Interface..."
        echo "Open your browser to: http://localhost:8000"
        echo "Press Ctrl+C to stop the web interface."
        python3 web_interface.py
        ;;
    3)
        echo "🧪 Running Test Client..."
        python3 test_client.py
        ;;
    4)
        echo "📚 Documentation:"
        echo "=================="
        echo "📖 README.md - Complete setup and usage guide"
        echo "🔗 Web Interface - http://localhost:8000 (when running)"
        echo "📧 Gmail Tools - Read inbox, send emails, manage drafts"
        echo "📁 Drive Tools - Upload, download, share files"
        echo "📝 Docs Tools - Create, edit, share documents"
        echo ""
        echo "For detailed API documentation, see README.md"
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
