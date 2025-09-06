# 🚀 Google Services MCP OAuth Integration API

This document describes the complete OAuth integration API provided by `main.py` for integrating Google Services (Gmail, Drive, Docs) with your applications.

## 📋 Overview

The `main.py` file provides a complete REST API for OAuth integration with Google Services. It handles the entire OAuth flow from initiation to token exchange and service usage, without requiring any templates or web interfaces.

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Your UI   │───▶│  main.py   │───▶│   Google   │───▶│ PostgreSQL  │
│ Application │    │    API     │    │   OAuth    │    │  Database   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 🚀 Quick Start

### 1. Start the API Server

```bash
python3 main.py
```

The server will start on `http://localhost:8000` (configurable via environment variables).

### 2. Access API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 🔐 Complete OAuth Flow

### Step 1: Create/Get Workspace

```bash
# Create a new workspace for a user
curl -X POST "http://localhost:8000/api/workspace" \
  -H "Content-Type: application/json" \
  -d '{"name": "john_doe"}'
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "john_doe",
  "status": "created"
}
```

### Step 2: Initiate OAuth Flow

```bash
# Start OAuth for Gmail
curl -X POST "http://localhost:8000/api/oauth/initiate" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "service": "gmail"}'
```

**Response:**
```json
{
  "success": true,
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe",
  "service": "gmail",
  "authorization_url": "https://accounts.google.com/o/oauth2/auth?...",
  "state": "eyJ1c2VybmFtZSI6ImpvaG5fZG9lIiwic2VydmljZSI6ImdtYWlsIn0=",
  "message": "OAuth flow initiated for gmail"
}
```

### Step 3: User Authorization

1. **Open the `authorization_url` in a browser**
2. **User signs in to Google and consents to permissions**
3. **Google redirects to your callback URL with an authorization code**

### Step 4: Handle OAuth Callback

```bash
# Google will redirect to:
http://localhost:8000/api/oauth/callback?code=AUTHORIZATION_CODE&state=STATE_PARAMETER
```

**Response:**
```json
{
  "success": true,
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe",
  "service": "gmail",
  "message": "Successfully authenticated with gmail",
  "tokens_received": true,
  "redirect_url": "/oauth-success?service=gmail&username=john_doe"
}
```

### Step 5: Check OAuth Status

```bash
# Check if user is authenticated
curl "http://localhost:8000/api/oauth/status/john_doe/gmail"
```

**Response:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe",
  "service": "gmail",
  "is_authenticated": true,
  "last_authenticated": "2025-09-04T20:00:00Z"
}
```

### Step 6: Test Service Functionality

```bash
# Test Gmail service
curl -X POST "http://localhost:8000/api/service/test" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "service": "gmail"}'
```

**Response:**
```json
{
  "success": true,
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe",
  "service": "gmail",
  "test_result": [
    {
      "id": "msg123",
      "subject": "Test Email",
      "from": "sender@example.com",
      "snippet": "This is a test email..."
    }
  ],
  "message": "Service gmail tested successfully"
}
```

## 📚 API Endpoints Reference

### Workspace Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/workspace` | Create a new workspace |
| `GET` | `/api/workspace/{username}` | Get workspace information |

### OAuth Integration

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/oauth/initiate` | Start OAuth flow for a service |
| `GET` | `/api/oauth/callback` | Handle OAuth callback |
| `GET` | `/api/oauth/status/{username}/{service}` | Check OAuth status for a service |
| `GET` | `/api/oauth/status/{username}` | Check OAuth status for all services |

### Service Testing

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/service/test` | Test service functionality |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and endpoints |
| `GET` | `/api/health` | Health check |

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Database Configuration
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/oneplace_core

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/oauth/callback

# Server Configuration
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your_secret_key_here
```

### Google OAuth Setup

1. **Create Google Cloud Project**
2. **Enable APIs**: Gmail, Drive, Docs
3. **Create OAuth 2.0 Credentials**
4. **Set redirect URI**: `http://localhost:8000/api/oauth/callback`

## 🧪 Testing

### Run the Test Script

```bash
python3 test_api.py
```

This will test all API endpoints and demonstrate the OAuth flow.

### Manual Testing with curl

```bash
# Test health check
curl http://localhost:8000/api/health

# Create workspace
curl -X POST "http://localhost:8000/api/workspace" \
  -H "Content-Type: application/json" \
  -d '{"name": "test_user"}'

# Initiate OAuth
curl -X POST "http://localhost:8000/api/oauth/initiate" \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "service": "gmail"}'
```

## 🌐 Frontend Integration

### JavaScript Example

```javascript
// Initiate OAuth flow
async function startOAuth(username, service) {
  const response = await fetch('/api/oauth/initiate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, service })
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Redirect user to Google OAuth
    window.location.href = data.authorization_url;
  }
}

// Check OAuth status
async function checkOAuthStatus(username, service) {
  const response = await fetch(`/api/oauth/status/${username}/${service}`);
  const data = await response.json();
  
  if (data.is_authenticated) {
    console.log(`${service} is authenticated`);
  } else {
    console.log(`${service} needs authentication`);
  }
}
```

### React Example

```jsx
import React, { useState, useEffect } from 'react';

function OAuthIntegration({ username }) {
  const [oauthStatus, setOauthStatus] = useState({});
  
  useEffect(() => {
    checkOAuthStatus();
  }, [username]);
  
  const checkOAuthStatus = async () => {
    const response = await fetch(`/api/oauth/status/${username}`);
    const data = await response.json();
    setOauthStatus(data.services_status);
  };
  
  const startOAuth = async (service) => {
    const response = await fetch('/api/oauth/initiate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, service })
    });
    
    const data = await response.json();
    if (data.success) {
      window.location.href = data.authorization_url;
    }
  };
  
  return (
    <div>
      <h2>OAuth Status for {username}</h2>
      {Object.entries(oauthStatus).map(([service, status]) => (
        <div key={service}>
          <span>{service}: </span>
          {status.is_authenticated ? (
            <span>✅ Authenticated</span>
          ) : (
            <button onClick={() => startOAuth(service)}>
              🔐 Authenticate {service}
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
```

## 🔒 Security Considerations

- **HTTPS**: Use HTTPS in production
- **CORS**: Configure CORS properly for your domains
- **Rate Limiting**: Implement rate limiting for production
- **Token Storage**: Tokens are stored securely in PostgreSQL
- **User Isolation**: Each user has separate credentials

## 🚀 Production Deployment

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

### Environment Variables

```bash
# Production environment
GOOGLE_CLIENT_ID=your_production_client_id
GOOGLE_CLIENT_SECRET=your_production_client_secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/api/oauth/callback
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your_secure_secret_key
DATABASE_URL=postgresql://user:pass@host:port/db
```

## 📝 Error Handling

The API returns proper HTTP status codes and error messages:

- `200`: Success
- `400`: Bad Request (invalid parameters)
- `401`: Unauthorized (not authenticated)
- `404`: Not Found (workspace not found)
- `500`: Internal Server Error

## 🤝 Support

- **API Documentation**: Available at `/docs` when server is running
- **Error Logs**: Check server console for detailed error information
- **Database**: Verify PostgreSQL connection and schema

## 🔄 Migration from web_interface.py

The `main.py` provides the same functionality as `web_interface.py` but through REST APIs:

- ✅ **Same OAuth flow** - Complete Google OAuth integration
- ✅ **Same database operations** - Workspace and credential management
- ✅ **Same service integration** - Gmail, Drive, Docs functionality
- ❌ **No templates** - Pure API endpoints
- ✅ **Better integration** - Easy to integrate with any frontend
- ✅ **CORS support** - Can be called from web applications
- ✅ **Structured responses** - Consistent JSON API responses

---

**Ready to integrate Google Services with your application? Start with `python3 main.py` and follow the OAuth flow! 🚀**



