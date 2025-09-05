# 🔐 Google OAuth Setup Guide

## 🚨 Current Issue: OAuth Client Not Found

You're getting this error because the Google OAuth credentials are not configured:
```
Error 401: invalid_client
The OAuth client was not found.
```

## ✅ Solution: Set Up Google OAuth Credentials

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name your project (e.g., "FastMCP Google Services")
4. Click "Create"

### Step 2: Enable Google APIs

1. In your project, go to "APIs & Services" → "Library"
2. Search for and enable these APIs:
   - **Gmail API**
   - **Google Drive API**
   - **Google Docs API**

### Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Fill in the details:
   - **Name**: FastMCP Google Services
   - **Authorized JavaScript origins**: `http://localhost:8000`
   - **Authorized redirect URIs**: `http://localhost:8000/auth/callback`
5. Click "Create"

### Step 4: Get Your Credentials

After creating, you'll get:
- **Client ID** (looks like: `123456789-abcdefghijklmnop.apps.googleusercontent.com`)
- **Client Secret** (looks like: `GOCSPX-abcdefghijklmnopqrstuvwxyz`)

### Step 5: Create .env File

Create a `.env` file in your project root with:

```bash
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_actual_client_id_here
GOOGLE_CLIENT_SECRET=your_actual_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# Google API Scopes
GMAIL_SCOPE=https://www.googleapis.com/auth/gmail.modify
GDRIVE_SCOPE=https://www.googleapis.com/auth/drive
GDOCS_SCOPE=https://www.googleapis.com/auth/documents

# Server Configuration
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your_secret_key_here_change_this_in_production
```

### Step 6: Replace Placeholder Values

Replace the placeholder values with your actual credentials:
- `your_actual_client_id_here` → Your Google Client ID
- `your_actual_client_secret_here` → Your Google Client Secret
- `your_secret_key_here_change_this_in_production` → Any random string for security

## 🌐 Testing the Web Interface

### Step 1: Start the Web Interface

```bash
# Make sure you're in the project directory
cd /home/dante/Desktop/fast_mcp

# Activate virtual environment
source env/bin/activate

# Start the web interface
python3 web_interface.py
```

### Step 2: Access the Web Interface

1. Open your browser
2. Go to: `http://localhost:8000`
3. You should see the FastMCP Google Services interface

### Step 3: Test OAuth Flow

1. Click "Start OAuth Authentication"
2. You'll be redirected to Google's consent screen
3. Sign in with your Google account
4. Grant permissions for Gmail, Drive, and Docs
5. You'll be redirected back to the success page

### Step 4: Test the Tools

1. Go to the "Test Tools" page
2. Try different operations:
   - **Gmail**: Read inbox, send emails
   - **Drive**: List files, upload files
   - **Docs**: Create documents, read content

## 🛠️ Web Interface Features

### Available Test Pages

1. **Home Page** (`/`)
   - Overview of available services
   - Links to start OAuth and test tools

2. **OAuth Authentication** (`/auth`)
   - Initiates Google OAuth flow
   - Shows authorization URL

3. **Success Page** (`/success`)
   - Shows authentication result
   - Displays user information

4. **Test Tools Page** (`/test`)
   - Interactive forms to test each service
   - Real-time API testing

### Testing Different Services

#### Gmail Testing
- **Read Inbox**: View recent emails
- **Send Email**: Create and send emails
- **Search Emails**: Find specific emails
- **Check Labels**: View different email categories

#### Google Drive Testing
- **List Files**: Browse your Drive files
- **Upload File**: Upload files to Drive
- **Create Folder**: Create new folders
- **Share Files**: Share files with others

#### Google Docs Testing
- **Create Document**: Create new documents
- **Read Document**: View document content
- **Update Document**: Edit existing documents
- **Export Document**: Export to different formats

## 🔧 Troubleshooting

### Common Issues

#### 1. "OAuth client was not found"
- **Solution**: Make sure your Client ID and Secret are correct in `.env`
- **Check**: Verify credentials in Google Cloud Console

#### 2. "Redirect URI mismatch"
- **Solution**: Ensure redirect URI in Google Console matches your `.env`
- **Should be**: `http://localhost:8000/auth/callback`

#### 3. "API not enabled"
- **Solution**: Enable the required APIs in Google Cloud Console
- **Required**: Gmail API, Drive API, Docs API

#### 4. "Permission denied"
- **Solution**: Make sure you're signed in with the correct Google account
- **Check**: The account should have access to the APIs

### Debug Steps

1. **Check .env file**:
   ```bash
   cat .env
   ```

2. **Verify Google Cloud Console**:
   - APIs are enabled
   - OAuth credentials are correct
   - Redirect URI matches

3. **Check web interface logs**:
   ```bash
   python3 web_interface.py
   # Look for error messages in the terminal
   ```

4. **Test OAuth flow manually**:
   - Visit `http://localhost:8000/auth`
   - Follow the OAuth process
   - Check for error messages

## 🎯 Quick Test Commands

```bash
# 1. Set up credentials (one-time)
# Edit .env file with your Google credentials

# 2. Start web interface
python3 web_interface.py

# 3. Open browser
# Go to: http://localhost:8000

# 4. Test OAuth
# Click "Start OAuth Authentication"

# 5. Test tools
# Go to "Test Tools" page and try different operations
```

## 📋 Checklist

- [ ] Google Cloud Project created
- [ ] Required APIs enabled (Gmail, Drive, Docs)
- [ ] OAuth 2.0 credentials created
- [ ] `.env` file created with correct credentials
- [ ] Web interface started successfully
- [ ] OAuth flow completed
- [ ] Tools tested successfully

Once you complete this setup, you'll be able to test all the Google services through the web interface! 🚀
