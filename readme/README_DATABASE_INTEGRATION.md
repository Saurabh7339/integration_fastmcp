# 🗄️ Database-Integrated OAuth System (SQLite)

This project has been updated to integrate with your database models instead of storing credentials in local files. OAuth tokens are now stored in the `WorkspaceIntegrationLink` table using the `auth_details` TEXT field (JSON serialized for SQLite compatibility).

## 🏗️ **Architecture Changes**

### **Before (File-based)**
```
credentials/
├── user123_credentials.json
├── user456_credentials.json
└── default_credentials.json
```

### **After (Database-based with SQLite)**
```sql
-- Workspace table
workspace
├── id (UUID, primary key)
├── name (string)
└── integrations (relationship)

-- Integration table  
integration
├── id (UUID, primary key)
├── name (string)
└── workspaces (relationship)

-- WorkspaceIntegrationLink table
workspace_integration_link
├── workspace_id (UUID, foreign key)
├── integration_id (UUID, foreign key)
├── auth_details (TEXT) ← OAuth credentials stored as JSON string
└── created_date (datetime)
```

## 🔧 **Key Changes**

### **1. OAuth Class Updates**
- **Constructor**: Now requires `db_session: Session`
- **Token Storage**: Credentials saved to `WorkspaceIntegrationLink.auth_details` as JSON string
- **User ID**: Changed from `user_id` to `workspace_id` (UUID)
- **Automatic Integration**: Creates "Google" integration record automatically
- **SQLite Compatibility**: Handles JSON serialization/deserialization for SQLite

### **2. Server Updates**
- **Constructor**: All servers now require `db_session: Session`
- **Parameter Changes**: All tools use `workspace_id` instead of `user_id`
- **UUID Validation**: Added UUID format validation for workspace_id parameters

### **3. Database Integration**
- **SQLite Database**: Uses SQLite instead of PostgreSQL for simplicity
- **Automatic Table Creation**: Tables created automatically when needed
- **Integration Management**: Google integration created/retrieved automatically
- **Credential Storage**: OAuth tokens stored as JSON strings in TEXT field with automatic refresh

## 🚀 **Usage Examples**

### **Basic Setup**
```python
from database import create_tables, get_db_session
from auth.oauth import GoogleOAuth
from server import GoogleServicesMCP

# Create tables
create_tables()

# Get database session
db_session = get_db_session()

# Initialize OAuth
oauth = GoogleOAuth(db_session)

# Initialize MCP server
mcp_server = GoogleServicesMCP(db_session)
```

### **OAuth Flow**
```python
# 1. Get authorization URL
auth_url = oauth.get_authorization_url()

# 2. User completes OAuth and gets authorization_code
# 3. Exchange code for tokens (requires workspace_id)
tokens = oauth.exchange_code_for_tokens(
    authorization_code="...", 
    workspace_id="550e8400-e29b-41d4-a716-446655440000"
)

# 4. Credentials automatically saved to database
```

### **Using Services**
```python
# All service calls now require workspace_id
emails = mcp_server.read_inbox(
    workspace_id="550e8400-e29b-41d4-a716-446655440000",
    max_results=10
)

files = mcp_server.list_drive_files(
    workspace_id="550e8400-e29b-41d4-a716-446655440000",
    page_size=20
)

doc = mcp_server.create_google_doc(
    workspace_id="550e8400-e29b-41d4-a716-446655440000",
    title="New Document"
)
```

## 📊 **Database Schema (SQLite)**

### **Workspace Table**
```sql
CREATE TABLE workspace (
    id BLOB PRIMARY KEY,  -- UUID stored as BLOB
    name TEXT NOT NULL
);
```

### **Integration Table**
```sql
CREATE TABLE integration (
    id BLOB PRIMARY KEY,  -- UUID stored as BLOB
    name TEXT NOT NULL
);
```

### **WorkspaceIntegrationLink Table**
```sql
CREATE TABLE workspace_integration_link (
    workspace_id BLOB REFERENCES workspace(id),  -- UUID stored as BLOB
    integration_id BLOB REFERENCES integration(id),  -- UUID stored as BLOB
    auth_details TEXT DEFAULT '{}',  -- JSON string for SQLite compatibility
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (workspace_id, integration_id)
);
```

## 🔐 **OAuth Credential Storage (SQLite)**

Credentials are stored in the `auth_details` TEXT field as a JSON string:
```json
{
    "token": "ya29.A0AfH6SMB...",
    "refresh_token": "1//04dX...",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "your-client-id.apps.googleusercontent.com",
    "client_secret": "your-client-secret",
    "scopes": [
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/documents"
    ]
}
```

**Note**: SQLite stores this as a TEXT field, so the system automatically serializes/deserializes the JSON data.

## 🔄 **Automatic Token Refresh**

The system automatically:
1. **Checks token expiration** when `get_valid_credentials()` is called
2. **Refreshes expired tokens** using the refresh token
3. **Updates database** with new tokens automatically
4. **Handles errors** gracefully by removing invalid credentials
5. **Maintains SQLite compatibility** with JSON serialization

## 🛠️ **Environment Setup**

### **Required Environment Variables**
```bash
# Database (SQLite)
DATABASE_URL=sqlite:///./fastmcp.db

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
```

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

**Note**: No PostgreSQL dependencies required - SQLite is included with Python.

## 📝 **Migration from File-based System**

If you're migrating from the old file-based system:

1. **Backup existing credentials** from `credentials/` folder
2. **Create database tables** using `create_tables()`
3. **Create workspaces** for each user
4. **Migrate credentials** by calling `exchange_code_for_tokens()` for each user
5. **Remove old credentials folder** after successful migration

## 🧪 **Testing**

Run the example script to test the system:
```bash
python example_usage.py
```

This will:
- Create SQLite database and tables
- Create a test workspace
- Initialize the OAuth system
- Show available MCP tools
- Provide usage instructions

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Database Connection Error**
   - Check `DATABASE_URL` environment variable
   - Ensure write permissions in the current directory
   - SQLite database file will be created automatically

2. **UUID Format Error**
   - Ensure workspace_id is a valid UUID string
   - Use proper UUID format: `550e8400-e29b-41d4-a716-446655440000`

3. **Table Not Found**
   - Run `create_tables()` before using the system
   - Check that the SQLite database file exists

4. **OAuth Errors**
   - Verify Google OAuth credentials in `.env`
   - Check redirect URI matches Google Console settings
   - Ensure required APIs are enabled

5. **JSON Parsing Errors**
   - The system automatically handles JSON serialization for SQLite
   - If you see JSON errors, the auth_details field may be corrupted

## 📚 **API Reference**

### **OAuth Methods**
- `get_authorization_url()` → Returns OAuth authorization URL
- `exchange_code_for_tokens(auth_code, workspace_id)` → Exchanges code for tokens
- `get_valid_credentials(workspace_id)` → Gets valid credentials (with auto-refresh)
- `get_workspace_credentials_status(workspace_id)` → Gets credential status
- `revoke_credentials(workspace_id)` → Removes credentials

### **Database Methods**
- `create_tables()` → Creates all database tables
- `get_db_session()` → Returns database session
- `create_workspace(name)` → Creates new workspace
- `get_workspace_by_id(workspace_id)` → Gets workspace by ID
- `save_workspace_credentials(workspace_id, auth_details)` → Saves credentials
- `remove_workspace_credentials(workspace_id)` → Removes credentials

## 💾 **SQLite Benefits**

- **No Installation Required**: SQLite comes with Python
- **Single File**: Database stored in one file (`fastmcp.db`)
- **Portable**: Easy to backup and move
- **Simple Setup**: No database server configuration needed
- **Development Friendly**: Perfect for development and testing

## 🔄 **SQLite vs PostgreSQL**

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Installation** | Built-in | Requires server setup |
| **Configuration** | None needed | Complex configuration |
| **JSON Support** | TEXT + JSON serialization | Native JSONB |
| **UUID Support** | BLOB storage | Native UUID type |
| **Performance** | Good for small-medium | Excellent for large scale |
| **Use Case** | Development, small apps | Production, large scale |

The system now provides a robust, scalable solution for managing OAuth credentials across multiple workspaces with automatic token refresh and secure SQLite database storage.
