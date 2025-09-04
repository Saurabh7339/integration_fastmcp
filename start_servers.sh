#!/bin/bash

# Google Services MCP Servers Startup Script
# This script manages three separate MCP servers for Gmail, Google Drive, and Google Docs

echo "🚀 Google Services MCP Servers"
echo "=============================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if requirements are installed
if [ ! -f ".env" ]; then
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
echo "1) 📧 Start Gmail MCP Server"
echo "2) 📁 Start Google Drive MCP Server"
echo "3) 📝 Start Google Docs MCP Server"
echo "4) 🚀 Start All Three Servers (in separate terminals)"
        echo "5) 🧪 Run Test Client"
        echo "6) 🔍 Test Server Connections"
        echo "7) 🎯 Run Demo Script"
        echo "8) 🔐 Setup OAuth Credentials"
        echo "9) 🌐 Start Web Interface"
        echo "10) 📚 Show Documentation"
        echo "11) 🚪 Exit"
echo ""

        read -p "Enter your choice (1-11): " choice

case $choice in
    1)
        echo "📧 Starting Gmail MCP Server..."
        echo "Server will be available for Gmail-related MCP connections."
        echo "Press Ctrl+C to stop the server."
        python3 gmail_server.py
        ;;
    2)
        echo "📁 Starting Google Drive MCP Server..."
        echo "Server will be available for Drive-related MCP connections."
        echo "Press Ctrl+C to stop the server."
        python3 gdrive_server.py
        ;;
    3)
        echo "📝 Starting Google Docs MCP Server..."
        echo "Server will be available for Docs-related MCP connections."
        echo "Press Ctrl+C to stop the server."
        python3 gdocs_server.py
        ;;
    4)
        echo "🚀 Starting All Three MCP Servers..."
        echo "Each server will run in a separate terminal window."
        echo ""
        
        # Check if xterm is available for Linux
        if command -v xterm &> /dev/null; then
            echo "📧 Starting Gmail Server in new terminal..."
            xterm -title "Gmail MCP Server" -e "python3 gmail_server.py" &
            
            echo "📁 Starting Google Drive Server in new terminal..."
            xterm -title "Google Drive MCP Server" -e "python3 gdrive_server.py" &
            
            echo "📝 Starting Google Docs Server in new terminal..."
            xterm -title "Google Docs MCP Server" -e "python3 gdocs_server.py" &
            
            echo "✅ All servers started in separate terminals!"
            echo "Each server is running independently with its own MCP namespace."
            echo ""
            echo "Server Namespaces:"
            echo "  - Gmail: gmail-mcp-server"
            echo "  - Drive: gdrive-mcp-server"
            echo "  - Docs: gdocs-mcp-server"
            echo ""
            echo "You can now connect to each server independently."
            
        elif command -v gnome-terminal &> /dev/null; then
            echo "📧 Starting Gmail Server in new terminal..."
            gnome-terminal --title="Gmail MCP Server" -- python3 gmail_server.py &
            
            echo "📁 Starting Google Drive Server in new terminal..."
            gnome-terminal --title="Google Drive MCP Server" -- python3 gdrive_server.py &
            
            echo "📝 Starting Google Docs Server in new terminal..."
            gnome-terminal --title="Google Docs MCP Server" -- python3 gdocs_server.py &
            
            echo "✅ All servers started in separate terminals!"
            echo "Each server is running independently with its own MCP namespace."
            
        else
            echo "⚠️  No suitable terminal emulator found."
            echo "Please start each server manually in separate terminal windows:"
            echo ""
            echo "Terminal 1: python3 gmail_server.py"
            echo "Terminal 2: python3 gdrive_server.py"
            echo "Terminal 3: python3 gdocs_server.py"
            echo ""
            echo "Or install xterm: sudo apt-get install xterm"
        fi
        ;;
    5)
        echo "🧪 Running Test Client..."
        echo "Testing server connections and MCP communication."
        echo "Choose from the available test options:"
        echo "1) Test server connections"
        echo "2) Test MCP communication"
        echo "3) Show demo"
        read -p "Enter choice (1-3): " test_choice
        case $test_choice in
            1)
                python3 test_server_connection.py
                ;;
            2)
                python3 mcp_client_example.py
                ;;
            3)
                python3 demo_servers.py
                ;;
            *)
                echo "Running server connection test..."
                python3 test_server_connection.py
                ;;
        esac
        ;;
    6)
        echo "🔍 Testing Server Connections..."
        echo "This will test the actual communication with the running servers."
        python3 test_server_connection.py
        ;;
    7)
        echo "🎯 Running Demo Script..."
        echo "This will show you the architecture and capabilities of the separate servers."
        python3 demo_servers.py
        ;;
    8)
        echo "🔐 Setting up OAuth Credentials..."
        echo "This will help you create the .env file with your Google credentials."
        python3 setup_oauth.py
        ;;
    9)
        echo "🌐 Starting Web Interface..."
        echo "Open your browser to: http://localhost:8000"
        echo "Press Ctrl+C to stop the web interface."
        python3 web_interface.py
        ;;
    10)
        echo "📚 Documentation:"
        echo "=================="
        echo "📖 README.md - Complete setup and usage guide"
        echo "🔗 Web Interface - http://localhost:8000 (when running)"
        echo ""
        echo "🚀 Separate MCP Servers:"
        echo "📧 Gmail Server (gmail-mcp-server):"
        echo "   - read_inbox, create_email, check_sent_emails"
        echo "   - check_drafts, check_promotions, check_important_emails"
        echo "   - search_emails, get_email_details"
        echo ""
        echo "📁 Google Drive Server (gdrive-mcp-server):"
        echo "   - list_drive_files, create_drive_folder, upload_drive_file"
        echo "   - download_drive_file, share_drive_file, search_drive_files"
        echo "   - delete_drive_file, move_drive_file, get_drive_file_info"
        echo "   - get_shared_drive_files, get_starred_drive_files"
        echo ""
        echo "📝 Google Docs Server (gdocs-mcp-server):"
        echo "   - create_google_doc, get_google_doc, update_google_doc"
        echo "   - list_google_docs, search_google_docs, share_google_doc"
        echo "   - export_google_doc, add_comment_to_doc, delete_google_doc"
        echo "   - get_doc_permissions, duplicate_google_doc"
        echo ""
        echo "🔐 Each server has its own authentication tools:"
        echo "   - get_auth_url, authenticate_user, get_user_credentials"
        echo ""
        echo "For detailed API documentation, see README.md"
        ;;
    11)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
