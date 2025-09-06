# MCP Server Testing Guide

This guide explains how to test the Google Docs, Gmail, and Google Drive MCP servers including the OAuth flow.

## Prerequisites

### 1. Install Dependencies

```bash
pip install sqlmodel psycopg2-binary google-auth google-auth-oauthlib google-auth-httplib2 python-dotenv
```

### 2. Set Up Environment Variables

Create a `.env` file or set environment variables:

```bash
# OAuth Credentials (at minimum, set these)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Optional: Service-specific credentials
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
GDRIVE_CLIENT_ID=your_gdrive_client_id
GDRIVE_CLIENT_SECRET=your_gdrive_client_secret
GDOCS_CLIENT_ID=your_gdocs_client_id
GDOCS_CLIENT_SECRET=your_gdocs_client_secret

# Database
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/oneplace_core

# Redirect URI
GOOGLE_REDIRECT_URI=http://localhost:8000/google/callback
```

### 3. Set Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Gmail API
   - Google Drive API
   - Google Docs API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:8000/google/callback`
   - `http://localhost:8080/callback`

## Testing Methods

### Method 1: Basic Structure Test

Test the basic structure without dependencies:

```bash
python simple_test.py
```

This will verify:
- ✅ FastMCP functionality
- ✅ Server file structure
- ✅ Environment configuration
- ✅ Basic imports

### Method 2: Full OAuth Test

Test all MCP servers with OAuth flow:

```bash
python test_mcp_oauth.py
```

This will test:
- ✅ Server initialization
- ✅ Tool registration
- ✅ OAuth URL generation
- ✅ Credentials status checking
- ✅ OAuth flow simulation
- ✅ Service tools
- ✅ Clear credentials functionality

### Method 3: Interactive Test

Run interactive test interface:

```bash
python test_web_oauth.py
```

This provides a command-line interface to:
- Get OAuth URLs
- Test OAuth flow with authorization codes
- Check credentials status
- Test service tools
- Clear credentials

### Method 4: Web Interface Test

Start a web server for browser-based testing:

```bash
python oauth_test_server.py
```

Then open `http://localhost:8080` in your browser to:
- Get OAuth URLs for each service
- Test OAuth flow through web interface
- Check credentials status
- Test service tools
- Clear credentials

## OAuth Flow Testing

### Step 1: Get OAuth URL

```bash
# Using the test script
python test_web_oauth.py
# Choose option 1, then select service (docs/gmail/drive)
```

Or use the web interface at `http://localhost:8080`

### Step 2: Authorize

1. Copy the OAuth URL from the test output
2. Open it in your browser
3. Sign in to your Google account
4. Grant permissions for the requested scopes
5. You'll be redirected to the callback URL with an authorization code

### Step 3: Test OAuth Flow

```bash
# Using the test script
python test_web_oauth.py
# Choose option 2, enter service and authorization code
```

### Step 4: Test Service Tools

```bash
# Using the test script
python test_web_oauth.py
# Choose option 4, select service
```

## Individual Server Testing

### Test Google Docs Server

```bash
python gdocs_server.py
```

This will:
- Initialize the server
- Display available tools
- Show tool descriptions

### Test Gmail Server

```bash
python gmail_server.py
```

### Test Google Drive Server

```bash
python gdrive_server.py
```

### Test Combined Server

```bash
python server.py
```

## Available Tools

### Google Docs Tools
- `get_docs_auth_url()` - Get OAuth authorization URL
- `authenticate_docs_user(authorization_code, workspace_id)` - Exchange code for tokens
- `get_docs_credentials_status(workspace_id)` - Check credentials status
- `create_google_doc(workspace_id, title, content)` - Create a new document
- `get_google_doc(workspace_id, document_id)` - Get document content
- `update_google_doc(workspace_id, document_id, content, append)` - Update document
- `list_google_docs(workspace_id, page_size)` - List documents
- `search_google_docs(workspace_id, query, page_size)` - Search documents
- `share_google_doc(workspace_id, document_id, email, role)` - Share document
- `export_google_doc(workspace_id, document_id, export_format, output_path)` - Export document
- `clear_google_credentials(workspace_id)` - Clear credentials

### Gmail Tools
- `get_gmail_auth_url()` - Get OAuth authorization URL
- `authenticate_gmail_user(authorization_code, workspace_id)` - Exchange code for tokens
- `get_gmail_credentials_status(workspace_id)` - Check credentials status
- `read_inbox(workspace_id, max_results, query)` - Read inbox emails
- `create_email(workspace_id, to, subject, body, cc, bcc)` - Send email
- `check_sent_emails(workspace_id, max_results)` - Check sent emails
- `check_drafts(workspace_id, max_results)` - Check draft emails
- `check_promotions(workspace_id, max_results)` - Check promotional emails
- `check_important_emails(workspace_id, max_results)` - Check important emails
- `search_emails(workspace_id, query, max_results)` - Search emails
- `clear_google_credentials(workspace_id)` - Clear credentials

### Google Drive Tools
- `get_drive_auth_url()` - Get OAuth authorization URL
- `authenticate_drive_user(authorization_code, workspace_id)` - Exchange code for tokens
- `get_drive_credentials_status(workspace_id)` - Check credentials status
- `list_drive_files(workspace_id, page_size, query)` - List files
- `create_drive_folder(workspace_id, name, parent_id)` - Create folder
- `upload_drive_file(workspace_id, file_path, name, parent_id)` - Upload file
- `download_drive_file(workspace_id, file_id, destination_path)` - Download file
- `share_drive_file(workspace_id, file_id, email, role)` - Share file
- `search_drive_files(workspace_id, query, page_size)` - Search files
- `clear_google_credentials(workspace_id)` - Clear credentials

## Troubleshooting

### Common Issues

1. **"No module named 'sqlmodel'"**
   ```bash
   pip install sqlmodel
   ```

2. **"No module named 'google_auth_oauthlib'"**
   ```bash
   pip install google-auth-oauthlib
   ```

3. **"No OAuth credentials found"**
   - Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` environment variables
   - Or set service-specific credentials

4. **"Scope has changed" error**
   ```bash
   python clear_credentials.py clear-all
   ```

5. **Database connection errors**
   - Check `DATABASE_URL` environment variable
   - Ensure PostgreSQL is running
   - Verify database credentials

### Debug Steps

1. **Check environment variables:**
   ```bash
   python simple_test.py
   ```

2. **Test basic functionality:**
   ```bash
   python test_mcp_oauth.py
   ```

3. **Check OAuth URLs:**
   ```bash
   python test_web_oauth.py
   # Choose option 1
   ```

4. **Verify database connection:**
   ```bash
   python -c "from database import get_db_session; session = get_db_session(); print('Database OK'); session.close()"
   ```

## Expected Results

### Successful OAuth Flow

1. OAuth URL generated successfully
2. Authorization code received after user consent
3. Tokens exchanged successfully
4. Credentials status shows "has_credentials": true
5. Service tools return data (not "No valid credentials" error)

### Successful Service Tool Test

- **Google Docs**: Returns list of documents or creates new document
- **Gmail**: Returns list of emails or sends email successfully
- **Google Drive**: Returns list of files or uploads/downloads files

## Next Steps

After successful testing:

1. **Integrate with your application** using the MCP server classes
2. **Set up production OAuth credentials** with proper redirect URIs
3. **Configure database** for production use
4. **Set up monitoring** for OAuth token expiration
5. **Implement error handling** for network issues and API limits
