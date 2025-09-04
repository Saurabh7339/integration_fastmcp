# 🚀 Quick OAuth Setup Guide

## 🚨 Current Issue: "OAuth client was not found"

Your `.env` file has placeholder values. You need real Google OAuth credentials.

## ✅ Quick Fix Steps

### Step 1: Get Google OAuth Credentials

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create/Select Project**
3. **Enable APIs**:
   - Gmail API
   - Google Drive API
   - Google Docs API
4. **Create OAuth 2.0 Credentials**:
   - "APIs & Services" → "Credentials"
   - "Create Credentials" → "OAuth 2.0 Client IDs"
   - **Type**: Web application
   - **Name**: FastMCP Google Services
   - **Authorized redirect URIs**: `http://localhost:8000/auth/callback`
5. **Copy Credentials**:
   - Client ID (ends with `.apps.googleusercontent.com`)
   - Client Secret (starts with `GOCSPX-`)

### Step 2: Update .env File

**Option A: Use the script**
```bash
python3 update_credentials.py
```

**Option B: Manual edit**
```bash
nano .env
# Replace these lines:
GOOGLE_CLIENT_ID=your_actual_client_id_here
GOOGLE_CLIENT_SECRET=your_actual_client_secret_here
```

### Step 3: Test

```bash
# Start web interface
python3 web_interface.py

# Open browser
# Go to: http://localhost:8000

# Test OAuth
# Click "Start OAuth Authentication"
```

## 🔍 Common Issues

### "OAuth client was not found"
- **Cause**: Wrong Client ID or Client Secret
- **Fix**: Double-check credentials in Google Cloud Console

### "Redirect URI mismatch"
- **Cause**: Wrong redirect URI in Google Console
- **Fix**: Set exactly: `http://localhost:8000/auth/callback`

### "API not enabled"
- **Cause**: APIs not enabled in Google Cloud Console
- **Fix**: Enable Gmail, Drive, and Docs APIs

## 📋 Checklist

- [ ] Google Cloud Project created
- [ ] APIs enabled (Gmail, Drive, Docs)
- [ ] OAuth 2.0 credentials created (Web application)
- [ ] Redirect URI set: `http://localhost:8000/auth/callback`
- [ ] .env file updated with real credentials
- [ ] Web interface started
- [ ] OAuth flow tested

## 🎯 Expected Result

After setup, you should be able to:
1. Click "Start OAuth Authentication"
2. See Google consent screen
3. Grant permissions
4. Return to success page
5. Test Gmail, Drive, and Docs tools
