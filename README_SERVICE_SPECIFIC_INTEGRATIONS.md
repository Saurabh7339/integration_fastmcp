# 🎯 Service-Specific Google Integrations

This system now supports **separate OAuth integrations** for each Google service instead of one generic "Google" integration. Each service (Gmail, Google Drive, Google Docs) has its own:

- **OAuth credentials** and refresh tokens
- **Scopes** and permissions
- **Integration records** in the database
- **Independent authentication flows**

## 🏗️ **New Architecture**

### **Before: Single Google Integration**
```sql
-- Integration table
id: 550e8400-e29b-41d4-a716-446655440001, name: "Google"

-- WorkspaceIntegrationLink table
workspace_id | integration_id | auth_details
-------------|---------------|-------------
workspace_A  | Google        | {gmail+drive+docs tokens}
workspace_B  | Google        | {gmail+drive+docs tokens}
```

### **After: Service-Specific Integrations**
```sql
-- Integration table
id: 550e8400-e29b-41d4-a716-446655440001, name: "Google Gmail"
id: 550e8400-e29b-41d4-a716-446655440002, name: "Google Drive"
id: 550e8400-e29b-41d4-a716-446655440003, name: "Google Docs"

-- WorkspaceIntegrationLink table
workspace_id | integration_id | auth_details
-------------|---------------|-------------
workspace_A  | Google Gmail  | {gmail tokens only}
workspace_A  | Google Drive  | {drive tokens only}
workspace_B  | Google Gmail  | {gmail tokens only}
workspace_B  | Google Docs   | {docs tokens only}
```

## 🔐 **Service-Specific OAuth Classes**

### **Gmail OAuth**
```python
from auth.oauth import GoogleOAuth

# Initialize Gmail-specific OAuth
gmail_oauth = GoogleOAuth(db_session, "gmail")

# Gmail scopes: https://www.googleapis.com/auth/gmail.modify
gmail_auth_url = gmail_oauth.get_authorization_url()
gmail_tokens = gmail_oauth.exchange_code_for_tokens(auth_code, workspace_id)
```

### **Google Drive OAuth**
```python
# Initialize Drive-specific OAuth
drive_oauth = GoogleOAuth(db_session, "drive")

# Drive scopes: https://www.googleapis.com/auth/drive
drive_auth_url = drive_oauth.get_authorization_url()
drive_tokens = drive_oauth.exchange_code_for_tokens(auth_code, workspace_id)
```

### **Google Docs OAuth**
```python
# Initialize Docs-specific OAuth
docs_oauth = GoogleOAuth(db_session, "docs")

# Docs scopes: https://www.googleapis.com/auth/documents
docs_auth_url = docs_oauth.get_authorization_url()
docs_tokens = docs_oauth.exchange_code_for_tokens(auth_code, workspace_id)
```

## 📊 **Database Schema**

### **Integration Table**
```sql
CREATE TABLE integration (
    id BLOB PRIMARY KEY,  -- UUID stored as BLOB
    name TEXT NOT NULL
);

-- Example records:
-- id: 550e8400-e29b-41d4-a716-446655440001, name: "Google Gmail"
-- id: 550e8400-e29b-41d4-a716-446655440002, name: "Google Drive"
-- id: 550e8400-e29b-41d4-a716-446655440003, name: "Google Docs"
```

### **WorkspaceIntegrationLink Table**
```sql
CREATE TABLE workspace_integration_link (
    workspace_id BLOB REFERENCES workspace(id),
    integration_id BLOB REFERENCES integration(id),
    auth_details TEXT DEFAULT '{}',  -- JSON string of OAuth tokens
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (workspace_id, integration_id)
);

-- Example records:
-- workspace_A | Google Gmail  | {"token": "ya29...", "refresh_token": "1//..."}
-- workspace_A | Google Drive  | {"token": "ya29...", "refresh_token": "1//..."}
-- workspace_B | Google Gmail  | {"token": "ya29...", "refresh_token": "1//..."}
```

## 🚀 **Usage Examples**

### **1. Initialize Multiple OAuth Systems**
```python
from auth.oauth import GoogleOAuth
from database import get_db_session

db_session = get_db_session()

# Create OAuth instances for each service
gmail_oauth = GoogleOAuth(db_session, "gmail")
drive_oauth = GoogleOAuth(db_session, "drive")
docs_oauth = GoogleOAuth(db_session, "docs")
```

### **2. Get Service-Specific Authorization URLs**
```python
# Each service has its own OAuth URL with appropriate scopes
gmail_url = gmail_oauth.get_authorization_url()
drive_url = drive_oauth.get_authorization_url()
docs_url = docs_oauth.get_author_url()

print(f"Gmail OAuth: {gmail_url}")
print(f"Drive OAuth: {drive_url}")
print(f"Docs OAuth: {docs_url}")
```

### **3. Authenticate Each Service Separately**
```python
# User can choose which services to connect
# Gmail authentication
gmail_tokens = gmail_oauth.exchange_code_for_tokens(auth_code, workspace_id)

# Drive authentication (separate OAuth flow)
drive_tokens = drive_oauth.exchange_code_for_tokens(auth_code, workspace_id)

# Docs authentication (separate OAuth flow)
docs_tokens = docs_oauth.exchange_code_for_tokens(auth_code, workspace_id)
```

### **4. Use Service-Specific Credentials**
```python
# Each service uses its own credentials
gmail_creds = gmail_oauth.get_valid_credentials(workspace_id)
drive_creds = drive_oauth.get_valid_credentials(workspace_id)
docs_creds = docs_oauth.get_valid_credentials(workspace_id)

# Use appropriate service with its credentials
if gmail_creds:
    gmail_service = GmailService(gmail_creds)
    emails = gmail_service.read_inbox()

if drive_creds:
    drive_service = GoogleDriveService(drive_creds)
    files = drive_service.list_files()
```

## 🎯 **MCP Server Tools**

### **Authentication Tools**
```python
# Service-specific OAuth URLs
get_gmail_auth_url()      # Returns Gmail OAuth URL
get_drive_auth_url()      # Returns Drive OAuth URL
get_docs_auth_url()       # Returns Docs OAuth URL

# Service-specific authentication
authenticate_gmail_user(auth_code, workspace_id)   # Gmail OAuth
authenticate_drive_user(auth_code, workspace_id)   # Drive OAuth
authenticate_docs_user(auth_code, workspace_id)    # Docs OAuth

# Check all service credentials
get_workspace_credentials_status(workspace_id)     # Returns status for all services
```

### **Service Tools**
```python
# Gmail tools (require Gmail credentials)
read_inbox(workspace_id, max_results, query)
create_email(workspace_id, to, subject, body)
search_emails(workspace_id, query, max_results)

# Drive tools (require Drive credentials)
list_drive_files(workspace_id, page_size, query)
upload_drive_file(workspace_id, file_path, name)
download_drive_file(workspace_id, file_id, destination)

# Docs tools (require Docs credentials)
create_google_doc(workspace_id, title, content)
update_google_doc(workspace_id, doc_id, content)
list_google_docs(workspace_id, page_size)
```

## 🔄 **OAuth Flow for Each Service**

### **Gmail OAuth Flow**
```
1. User calls get_gmail_auth_url()
2. User completes Gmail OAuth in browser
3. User calls authenticate_gmail_user(auth_code, workspace_id)
4. System creates "Google Gmail" integration if needed
5. System saves Gmail OAuth tokens to WorkspaceIntegrationLink
6. Gmail tools now work with these credentials
```

### **Google Drive OAuth Flow**
```
1. User calls get_drive_auth_url()
2. User completes Drive OAuth in browser
3. User calls authenticate_drive_user(auth_code, workspace_id)
4. System creates "Google Drive" integration if needed
5. System saves Drive OAuth tokens to WorkspaceIntegrationLink
6. Drive tools now work with these credentials
```

### **Google Docs OAuth Flow**
```
1. User calls get_docs_auth_url()
2. User completes Docs OAuth in browser
3. User calls authenticate_docs_user(auth_code, workspace_id)
4. System creates "Google Docs" integration if needed
5. System saves Docs OAuth tokens to WorkspaceIntegrationLink
6. Docs tools now work with these credentials
```

## 💡 **Benefits of Service-Specific Integrations**

### **1. Granular Access Control**
- **Workspaces can choose** which services to connect to
- **No forced bundling** of all Google services
- **Independent permissions** per service

### **2. Better Security**
- **Isolated credentials** for each service
- **Service-specific scopes** (minimal permissions)
- **Independent token refresh** cycles

### **3. Flexible Integration**
- **Partial integration** possible (just Gmail, no Drive)
- **Service-by-service** rollout
- **Easier permission management**

### **4. Scalability**
- **Add new services** without affecting existing ones
- **Service-specific configurations** and settings
- **Independent rate limiting** per service

## 🗄️ **Database Functions**

### **Service-Specific Functions**
```python
from database import (
    get_or_create_service_integration,
    get_workspace_service_credentials,
    save_workspace_service_credentials,
    remove_workspace_service_credentials
)

# Get or create integration for a specific service
gmail_integration = get_or_create_service_integration("gmail")

# Get credentials for a specific service
gmail_creds = get_workspace_service_credentials(workspace_id, "gmail")

# Save credentials for a specific service
save_workspace_service_credentials(workspace_id, "gmail", auth_details)

# Remove credentials for a specific service
remove_workspace_service_credentials(workspace_id, "gmail")
```

### **Aggregate Functions**
```python
from database import get_all_workspace_credentials

# Get all service credentials for a workspace
all_creds = get_all_workspace_credentials(workspace_id)

# Returns:
{
    "gmail": {
        "has_credentials": True,
        "integration_id": "550e8400-e29b-41d4-a716-446655440001",
        "created_date": "2024-01-15T10:30:00",
        "auth_details": {...}
    },
    "drive": {
        "has_credentials": False,
        "integration_id": "550e8400-e29b-41d4-a716-446655440002"
    },
    "docs": {
        "has_credentials": True,
        "integration_id": "550e8400-e29b-41d4-a716-446655440003",
        "created_date": "2024-01-15T11:00:00",
        "auth_details": {...}
    }
}
```

## 🧪 **Testing the System**

### **Run the Example**
```bash
python example_usage.py
```

This will:
- Create SQLite database with service-specific tables
- Initialize OAuth systems for Gmail, Drive, and Docs
- Show separate authorization URLs for each service
- Demonstrate credential status checking per service
- Display all available MCP tools

### **Manual Testing**
```python
from database import create_tables, get_db_session
from auth.oauth import GoogleOAuth

# Setup
create_tables()
db_session = get_db_session()

# Test each service
gmail_oauth = GoogleOAuth(db_session, "gmail")
drive_oauth = GoogleOAuth(db_session, "drive")
docs_oauth = GoogleOAuth(db_session, "docs")

# Check what integrations were created
print(f"Gmail integration: {gmail_oauth.service_integration.name}")
print(f"Drive integration: {drive_oauth.service_integration.name}")
print(f"Docs integration: {docs_oauth.service_integration.name}")
```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Service Not Found**
   - Ensure service type is one of: "gmail", "drive", "docs"
   - Check that integration was created in database

2. **Wrong Credentials for Service**
   - Each service uses its own OAuth instance
   - Verify you're using the correct service OAuth class

3. **Missing Service Integration**
   - Run `create_tables()` to create database structure
   - Check that integrations are created automatically

4. **Scope Mismatch**
   - Each service has specific scopes
   - Gmail: `gmail.modify`
   - Drive: `drive`
   - Docs: `documents`

## 📚 **API Reference**

### **GoogleOAuth Class**
```python
class GoogleOAuth:
    def __init__(self, db_session: Session, service_type: str)
    def get_authorization_url() -> str
    def exchange_code_for_tokens(auth_code: str, workspace_id: UUID) -> Dict
    def get_valid_credentials(workspace_id: UUID) -> Optional[Credentials]
    def get_workspace_credentials_status(workspace_id: UUID) -> Dict
    def revoke_credentials(workspace_id: UUID)
```

### **Service Types**
- `"gmail"` → Google Gmail integration
- `"drive"` → Google Drive integration  
- `"docs"` → Google Docs integration
- `"all"` → All scopes combined (for backward compatibility)

The system now provides **granular, secure, and flexible** OAuth integration for each Google service, allowing workspaces to choose exactly which services they want to connect to! 🚀
