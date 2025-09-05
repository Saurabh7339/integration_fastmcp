# 🤖 LLM Integration Guide for MCP Servers

## Overview

This guide explains how Large Language Models (LLMs) integrate with the three separate MCP servers for Gmail, Google Drive, and Google Docs, including OAuth authentication handling.

## 🔗 **Server Connection**

### **Server Namespaces**
LLMs connect to each server using their unique namespaces:

```python
# Gmail operations
gmail_server = "gmail-mcp-server"

# Google Drive operations  
drive_server = "gdrive-mcp-server"

# Google Docs operations
docs_server = "gdocs-mcp-server"
```

### **Transport Method**
- **STDIO transport** (standard input/output)
- Each server runs independently
- LLMs can connect to multiple servers simultaneously

## 🔐 **OAuth Authentication Flow**

### **Step 1: Check Existing Credentials**
```python
# LLM calls this tool first
get_user_credentials(user_id="user123")
# Returns: {"has_credentials": true/false, "user_id": "user123"}
```

### **Step 2: Get Authorization URL (if needed)**
```python
# If no credentials, LLM calls this
get_auth_url(user_id="user123")
# Returns: "https://accounts.google.com/o/oauth2/v2/auth?client_id=..."
```

### **Step 3: User Completes OAuth**
- User visits the authorization URL
- Signs in with Google account
- Grants permissions for Gmail, Drive, and Docs
- Gets redirected with authorization code

### **Step 4: Exchange Code for Tokens**
```python
# LLM calls this with the authorization code
authenticate_user(
    user_id="user123", 
    authorization_code="4/0AVMBsJ..."
)
# Returns: {"success": true, "user_id": "user123"}
```

### **Step 5: Use Service Tools**
```python
# Now LLM can call service-specific tools
read_inbox(user_id="user123", max_results=10)
list_drive_files(user_id="user123", page_size=20)
create_google_doc(user_id="user123", title="New Document")
```

## 🛠️ **Tool Usage Patterns**

### **Gmail Tools**
```python
# Authentication tools
get_auth_url(user_id="user123")
authenticate_user(user_id="user123", authorization_code="...")
get_user_credentials(user_id="user123")

# Email tools
read_inbox(user_id="user123", max_results=10)
create_email(user_id="user123", to="user@example.com", subject="Hello", body="Message")
check_sent_emails(user_id="user123", max_results=5)
check_drafts(user_id="user123", max_results=5)
search_emails(user_id="user123", query="from:important@example.com")
get_email_details(user_id="user123", email_id="...")
```

### **Google Drive Tools**
```python
# Authentication tools (same as Gmail)
get_auth_url(user_id="user123")
authenticate_user(user_id="user123", authorization_code="...")
get_user_credentials(user_id="user123")

# File tools
list_drive_files(user_id="user123", page_size=20)
create_drive_folder(user_id="user123", folder_name="New Folder")
upload_drive_file(user_id="user123", file_path="/path/to/file.txt")
download_drive_file(user_id="user123", file_id="...")
share_drive_file(user_id="user123", file_id="...", email="user@example.com")
search_drive_files(user_id="user123", query="document")
delete_drive_file(user_id="user123", file_id="...")
move_drive_file(user_id="user123", file_id="...", new_parent_id="...")
get_drive_file_info(user_id="user123", file_id="...")
```

### **Google Docs Tools**
```python
# Authentication tools (same as others)
get_auth_url(user_id="user123")
authenticate_user(user_id="user123", authorization_code="...")
get_user_credentials(user_id="user123")

# Document tools
create_google_doc(user_id="user123", title="New Document", content="Initial content")
get_google_doc(user_id="user123", document_id="...")
update_google_doc(user_id="user123", document_id="...", content="Updated content")
list_google_docs(user_id="user123", page_size=10)
search_google_docs(user_id="user123", query="meeting notes")
share_google_doc(user_id="user123", document_id="...", email="user@example.com")
export_google_doc(user_id="user123", document_id="...", format="pdf")
add_comment_to_doc(user_id="user123", document_id="...", comment="Great work!")
delete_google_doc(user_id="user123", document_id="...")
get_doc_permissions(user_id="user123", document_id="...")
duplicate_google_doc(user_id="user123", document_id="...", new_title="Copy")
```

## 🔧 **Credential Management**

### **Automatic Token Handling**
- **No manual token management** required by LLMs
- **Automatic token refresh** when tokens expire
- **Secure storage** in local files per user
- **User isolation** - each user has separate credentials

### **Credential Storage**
```python
# Credentials are stored automatically by the servers
# File structure:
credentials/
├── user123_gmail.json
├── user123_drive.json
└── user123_docs.json
```

### **Token Refresh**
- Tokens are automatically refreshed when they expire
- LLMs don't need to handle refresh logic
- Seamless operation without interruption

## 🎯 **Integration Examples**

### **Example 1: Email Assistant**
```python
# LLM workflow for email management
async def email_assistant(user_id):
    # Check credentials
    creds = await get_user_credentials(user_id)
    if not creds["has_credentials"]:
        # Guide user through OAuth
        auth_url = await get_auth_url(user_id)
        # User completes OAuth...
        await authenticate_user(user_id, auth_code)
    
    # Read inbox
    emails = await read_inbox(user_id, max_results=10)
    
    # Process emails
    for email in emails:
        # LLM analyzes email content
        # Takes actions based on content
        pass
```

### **Example 2: Document Creator**
```python
# LLM workflow for document creation
async def document_creator(user_id, topic):
    # Check credentials
    creds = await get_user_credentials(user_id)
    if not creds["has_credentials"]:
        # Handle authentication...
        pass
    
    # Create document
    doc = await create_google_doc(
        user_id=user_id,
        title=f"Document about {topic}",
        content="Initial content..."
    )
    
    # Update with generated content
    await update_google_doc(
        user_id=user_id,
        document_id=doc["id"],
        content="Generated content about the topic..."
    )
    
    return doc
```

### **Example 3: File Organizer**
```python
# LLM workflow for file organization
async def file_organizer(user_id):
    # Check credentials
    creds = await get_user_credentials(user_id)
    if not creds["has_credentials"]:
        # Handle authentication...
        pass
    
    # List files
    files = await list_drive_files(user_id, page_size=100)
    
    # Create organization folder
    folder = await create_drive_folder(user_id, "Organized Files")
    
    # Move files based on LLM analysis
    for file in files:
        # LLM decides where to move file
        await move_drive_file(user_id, file["id"], folder["id"])
```

## 🚨 **Error Handling**

### **Authentication Errors**
```python
# Handle expired tokens
try:
    result = await read_inbox(user_id, max_results=10)
except AuthenticationError:
    # Re-authenticate user
    auth_url = await get_auth_url(user_id)
    # Guide user through OAuth again
```

### **Service Errors**
```python
# Handle service-specific errors
try:
    result = await create_google_doc(user_id, title, content)
except ServiceError as e:
    # Handle specific service errors
    print(f"Service error: {e}")
```

## 🔄 **Multi-Service Workflows**

### **Cross-Service Operations**
```python
# LLM can combine multiple services
async def email_to_doc_workflow(user_id, email_id):
    # Get email content
    email = await get_email_details(user_id, email_id)
    
    # Create document from email
    doc = await create_google_doc(
        user_id=user_id,
        title=f"Email: {email['subject']}",
        content=email['body']
    )
    
    # Save to Drive folder
    folder = await create_drive_folder(user_id, "Email Documents")
    # Move document to folder...
    
    return doc
```

## 📋 **Best Practices**

### **1. Always Check Credentials First**
```python
# Before using any tool
creds = await get_user_credentials(user_id)
if not creds["has_credentials"]:
    # Handle authentication
```

### **2. Use Appropriate User IDs**
```python
# Use consistent user IDs across sessions
user_id = "user123"  # Keep consistent
```

### **3. Handle Errors Gracefully**
```python
# Always wrap tool calls in try-catch
try:
    result = await tool_call(user_id, params)
except Exception as e:
    # Handle error appropriately
```

### **4. Batch Operations**
```python
# Group related operations
emails = await read_inbox(user_id, max_results=50)
# Process all emails at once
```

## 🎯 **Summary**

### **Key Points for LLMs:**

1. **Connect to each server separately** using their namespaces
2. **Use user_id for all operations** to maintain user isolation
3. **Handle OAuth flow** when users don't have credentials
4. **No manual token management** - servers handle this automatically
5. **Combine multiple services** for complex workflows
6. **Handle errors gracefully** and re-authenticate when needed

### **OAuth Flow Summary:**
1. Check credentials → 2. Get auth URL (if needed) → 3. User completes OAuth → 4. Exchange code for tokens → 5. Use service tools

The MCP servers provide a clean, secure interface for LLMs to interact with Google services without worrying about the complexities of OAuth token management! 🚀
