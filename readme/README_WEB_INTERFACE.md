# 🌐 Web Interface - Service-Specific Google OAuth

This document describes the updated web interface that provides a user-friendly way to authenticate with Google services (Gmail, Drive, Docs) using username-based workspace management and SQLite database storage.

## 🏗️ **Architecture Overview**

### **Key Features**
- **Username-based Workspaces**: Each user gets a unique workspace identified by username
- **Service-Specific OAuth**: Separate authentication for Gmail, Drive, and Docs
- **SQLite Database**: All credentials stored securely in local database
- **Modern Web UI**: Beautiful, responsive interface with real-time status updates
- **Dashboard Management**: Centralized view of all service connections

### **Flow Diagram**
```
User enters username → Workspace created/retrieved → Service selection → 
OAuth flow → Credentials stored → Dashboard shows status → Service testing
```

## 🚀 **Getting Started**

### **1. Prerequisites**
```bash
# Install dependencies
pip install -r requirements.txt

# Ensure you have Google OAuth credentials configured
# Check config.py for CLIENT_ID and CLIENT_SECRET
```

### **2. Start the Web Interface**
```bash
python web_interface.py
```

The server will start on `http://localhost:8000` by default.

### **3. Access the Interface**
Open your browser and navigate to `http://localhost:8000`

## 🎯 **User Experience Flow**

### **Step 1: Home Page**
- Enter your username (e.g., `john_doe`, `company_name`)
- Choose which Google service to authenticate:
  - **📧 Gmail**: Email management
  - **📁 Google Drive**: File storage
  - **📝 Google Docs**: Document creation

### **Step 2: OAuth Authentication**
- Click on a service card
- You'll be redirected to Google OAuth
- Grant permissions for that specific service
- Redirected back to success page

### **Step 3: Dashboard**
- View all service connections in one place
- See which services are connected/disconnected
- Test service functionality
- Revoke access if needed

## 🔧 **Technical Implementation**

### **Database Schema**
```sql
-- Workspaces table
CREATE TABLE workspace (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL
);

-- Integrations table  
CREATE TABLE integration (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL  -- "Google Gmail", "Google Drive", "Google Docs"
);

-- Workspace-Integration links with credentials
CREATE TABLE workspace_integration_link (
    workspace_id UUID REFERENCES workspace(id),
    integration_id UUID REFERENCES integration(id),
    auth_details TEXT,  -- JSON-serialized OAuth credentials
    created_date DATETIME,
    PRIMARY KEY (workspace_id, integration_id)
);
```

### **API Endpoints**

#### **Authentication Routes**
```
GET  /auth/{service}?username={username}     # OAuth initiation
GET  /auth/{service}/callback?code={code}&state={username}  # OAuth callback
```

#### **Dashboard Routes**
```
GET  /dashboard/{username}                    # User dashboard
GET  /api/credentials/{username}              # Credentials status API
POST /api/revoke/{service}                   # Revoke service access
GET  /api/workspaces                         # List all workspaces
```

#### **Testing Routes**
```
POST /test/{service}                         # Test service functionality
```

### **OAuth Flow Implementation**
```python
# 1. User selects service and enters username
@app.get("/auth/{service}")
async def auth_page(service: str, username: str):
    workspace = get_or_create_workspace(username)
    oauth = GoogleOAuth(db_session, service)
    auth_url = oauth.get_authorization_url() + f"&state={username}"
    return render_auth_page(auth_url, service, username)

# 2. Google OAuth callback
@app.get("/auth/{service}/callback")
async def auth_callback(service: str, code: str, state: str):
    username = state  # Username passed through OAuth state
    workspace = get_or_create_workspace(username)
    oauth = GoogleOAuth(db_session, service)
    tokens = oauth.exchange_code_for_tokens(code, workspace.id)
    return redirect_to_success(service, username)

# 3. Credentials stored in database
def save_credentials(workspace_id, service_type, auth_details):
    integration = get_or_create_service_integration(service_type)
    save_workspace_service_credentials(workspace_id, service_type, auth_details)
```

## 🎨 **User Interface Components**

### **Home Page (`/`)**
- Username input field
- Service selection cards (Gmail, Drive, Docs)
- Information about the OAuth process
- Link to dashboard

### **Authentication Page (`/auth/{service}`)**
- Service-specific information
- Workspace details (username, workspace ID)
- OAuth authorization button
- Scope information for the service

### **Dashboard (`/dashboard/{username}`)**
- Workspace overview with statistics
- Service status cards (connected/disconnected)
- Action buttons for each service
- Credential information display

### **Success/Error Page (`/success`)**
- Authentication result display
- Service and username information
- Next steps guidance
- Navigation to dashboard

### **Test Page (`/test`)**
- Username input
- Service testing buttons
- Real-time results display
- Test all services option

## 🔐 **Security Features**

### **OAuth Security**
- **Service Isolation**: Each service has separate OAuth tokens
- **Scope Limitation**: Only necessary permissions requested
- **State Parameter**: Username passed securely through OAuth flow
- **Token Storage**: Encrypted storage in SQLite database

### **Database Security**
- **UUID Primary Keys**: Secure identifier generation
- **JSON Serialization**: Safe credential storage
- **Session Management**: Proper database session handling
- **Error Handling**: Secure error messages without data leakage

## 📱 **Responsive Design**

### **Mobile-First Approach**
- Responsive grid layouts
- Touch-friendly buttons
- Mobile-optimized forms
- Adaptive typography

### **Modern UI Elements**
- Glassmorphism design
- Smooth animations
- Interactive hover effects
- Loading states and feedback

## 🧪 **Testing and Debugging**

### **Test Script**
```bash
python test_web_interface.py
```

This script tests:
- Database functionality
- OAuth class initialization
- Web endpoint accessibility
- API responses

### **Manual Testing**
1. **Start the server**: `python web_interface.py`
2. **Open browser**: Navigate to `http://localhost:8000`
3. **Test OAuth flow**: Enter username, select service, complete OAuth
4. **Verify dashboard**: Check credential status and service connections
5. **Test services**: Use the test page to verify functionality

### **Debug Information**
- Console logs show authentication results
- Database queries logged (when debug mode enabled)
- OAuth flow state tracking
- Error details in success/error pages

## 🔄 **OAuth Flow Details**

### **Gmail Service**
```
Scope: https://www.googleapis.com/auth/gmail.modify
Permissions: Read, send, and manage emails
```

### **Google Drive Service**
```
Scope: https://www.googleapis.com/auth/drive
Permissions: View and manage Google Drive files
```

### **Google Docs Service**
```
Scope: https://www.googleapis.com/auth/documents
Permissions: View and manage Google Docs
```

## 📊 **Database Operations**

### **Workspace Management**
```python
# Create new workspace
workspace = create_workspace("john_doe")

# Get existing workspace
workspace = get_workspace_by_name("john_doe")

# Get or create (idempotent)
workspace = get_or_create_workspace("john_doe")
```

### **Credential Management**
```python
# Save credentials for a service
save_workspace_service_credentials(workspace_id, "gmail", auth_details)

# Get credentials for a service
creds = get_workspace_service_credentials(workspace_id, "gmail")

# Remove credentials
remove_workspace_service_credentials(workspace_id, "gmail")

# Get all credentials for a workspace
all_creds = get_all_workspace_credentials(workspace_id)
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. OAuth Errors**
- **Invalid redirect URI**: Check Google Console settings
- **Scope errors**: Verify service type in OAuth class
- **State parameter issues**: Check OAuth flow implementation

#### **2. Database Errors**
- **Table not found**: Run `create_tables()` function
- **UUID errors**: Check SQLite UUID compatibility
- **JSON serialization**: Verify auth_details format

#### **3. Web Interface Issues**
- **Port conflicts**: Change port in `config.py`
- **Template errors**: Check Jinja2 syntax in HTML files
- **Static files**: Ensure templates directory structure

### **Debug Commands**
```bash
# Check database tables
python -c "from database import create_tables; create_tables()"

# Test OAuth classes
python -c "from auth.oauth import GoogleOAuth; print('OAuth OK')"

# Verify web server
curl http://localhost:8000/
```

## 🔮 **Future Enhancements**

### **Planned Features**
- **User Authentication**: Login system with passwords
- **Service Templates**: Pre-configured service combinations
- **Bulk Operations**: Connect multiple services at once
- **Analytics Dashboard**: Usage statistics and monitoring
- **API Rate Limiting**: Protect against abuse
- **Multi-tenant Support**: Organization-level workspaces

### **Integration Possibilities**
- **SSO Integration**: SAML/OIDC support
- **Webhook Support**: Real-time credential updates
- **CLI Interface**: Command-line OAuth management
- **Mobile App**: Native mobile interface
- **API Gateway**: External service integration

## 📚 **API Documentation**

### **REST API Endpoints**

#### **GET /api/credentials/{username}**
Returns credential status for all services for a workspace.

**Response:**
```json
{
  "success": true,
  "username": "john_doe",
  "credentials": {
    "gmail": {
      "has_credentials": true,
      "integration_id": "uuid-here",
      "created_date": "2024-01-01T00:00:00"
    },
    "drive": {
      "has_credentials": false,
      "integration_id": "uuid-here"
    }
  }
}
```

#### **POST /api/revoke/{service}**
Revokes access for a specific service.

**Request:**
```json
{
  "username": "john_doe"
}
```

**Response:**
```json
{
  "success": true,
  "message": "gmail credentials revoked successfully"
}
```

#### **GET /api/workspaces**
Lists all workspaces (admin endpoint).

**Response:**
```json
{
  "success": true,
  "workspaces": [
    {
      "id": "uuid-here",
      "name": "john_doe"
    }
  ]
}
```

## 🎉 **Conclusion**

The updated web interface provides a comprehensive, user-friendly way to manage Google service integrations. With service-specific OAuth, username-based workspaces, and a modern dashboard, users can easily connect and manage their Google services while maintaining security and flexibility.

The system is designed to be scalable, secure, and maintainable, making it suitable for both individual users and enterprise deployments.
