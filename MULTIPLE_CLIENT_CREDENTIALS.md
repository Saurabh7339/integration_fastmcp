# Multiple Client Credentials Support

This document explains how to configure and use separate OAuth client credentials for each Google service (Gmail, Drive, Docs) in the MCP integration.

## Overview

The system now supports separate OAuth client credentials for each Google service, providing better security and service isolation. Each service can have its own OAuth client configuration while maintaining fallback support.

## Configuration

### Environment Variables

You can configure credentials in two ways:

#### 1. Service-Specific Credentials (Recommended)

Set separate credentials for each service:

```bash
# Gmail OAuth Credentials
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret

# Google Drive OAuth Credentials
GDRIVE_CLIENT_ID=your_gdrive_client_id
GDRIVE_CLIENT_SECRET=your_gdrive_client_secret

# Google Docs OAuth Credentials
GDOCS_CLIENT_ID=your_gdocs_client_id
GDOCS_CLIENT_SECRET=your_gdocs_client_secret
```

#### 2. Fallback Credentials

If service-specific credentials are not set, the system will use fallback credentials:

```bash
# Fallback OAuth Credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### Priority Order

1. **Service-specific credentials** (e.g., `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`)
2. **Fallback credentials** (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`)

## Implementation Details

### Config Class

The `Config` class now includes a `get_client_credentials()` method:

```python
@classmethod
def get_client_credentials(cls, service_type: str) -> tuple[str, str]:
    """
    Get client_id and client_secret for a specific service type.
    
    Args:
        service_type: The service type ('gmail', 'drive', 'docs')
        
    Returns:
        tuple: (client_id, client_secret)
        
    Raises:
        ValueError: If no credentials are found for the service
    """
```

### OAuth Class

The `GoogleOAuth` class automatically selects the appropriate credentials:

```python
class GoogleOAuth:
    def __init__(self, db_session: Session, service_type: str):
        # ... other initialization ...
        
        # OAuth configuration - Get service-specific credentials
        from config import Config
        self.client_id, self.client_secret = Config.get_client_credentials(service_type)
        self.redirect_uri = Config.GOOGLE_REDIRECT_URI
```

## Usage Examples

### Creating OAuth Instances

```python
# Each service will use its own credentials
gmail_oauth = GoogleOAuth(db_session, "gmail")      # Uses GMAIL_CLIENT_ID/SECRET
drive_oauth = GoogleOAuth(db_session, "drive")      # Uses GDRIVE_CLIENT_ID/SECRET
docs_oauth = GoogleOAuth(db_session, "docs")        # Uses GDOCS_CLIENT_ID/SECRET
```

### Error Handling

If no credentials are found, the system will raise a descriptive error:

```python
try:
    client_id, client_secret = Config.get_client_credentials("gmail")
except ValueError as e:
    print(f"Error: {e}")
    # Output: "No OAuth credentials found for service 'gmail'. 
    #          Please set GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET 
    #          environment variables, or set GOOGLE_CLIENT_ID and 
    #          GOOGLE_CLIENT_SECRET as fallback."
```

## Benefits

1. **Security**: Each service has its own OAuth client, limiting scope of access
2. **Isolation**: Issues with one service don't affect others
3. **Flexibility**: Can use different OAuth configurations per service
4. **Backward Compatibility**: Fallback to generic credentials if needed
5. **Easy Migration**: Can gradually migrate from single to multiple clients

## Testing

Use the provided test script to verify your configuration:

```bash
python test_client_credentials_simple.py
```

This will:
- Test credential selection for each service type
- Show which environment variables are set
- Provide recommendations for configuration

## Migration Guide

### From Single Client to Multiple Clients

1. **Create separate OAuth clients** in Google Cloud Console for each service
2. **Set service-specific environment variables**:
   ```bash
   GMAIL_CLIENT_ID=your_gmail_client_id
   GMAIL_CLIENT_SECRET=your_gmail_client_secret
   # ... etc for other services
   ```
3. **Keep fallback credentials** for backward compatibility:
   ```bash
   GOOGLE_CLIENT_ID=your_original_client_id
   GOOGLE_CLIENT_SECRET=your_original_client_secret
   ```
4. **Test each service** to ensure proper credential selection
5. **Clear existing credentials** if needed:
   ```bash
   python clear_credentials.py clear-all
   ```

## Troubleshooting

### Common Issues

1. **"No OAuth credentials found"**: Set the required environment variables
2. **Scope changes**: Use `clear_credentials.py` to clear old credentials
3. **Service not working**: Check if service-specific credentials are set correctly

### Debug Steps

1. Check environment variables:
   ```bash
   python test_client_credentials_simple.py
   ```

2. Verify OAuth client configuration in Google Cloud Console

3. Test credential selection:
   ```python
   from config import Config
   client_id, client_secret = Config.get_client_credentials("gmail")
   print(f"Gmail Client ID: {client_id}")
   ```

## Security Best Practices

1. **Use separate OAuth clients** for each service
2. **Limit scopes** to only what each service needs
3. **Rotate credentials** regularly
4. **Monitor OAuth usage** in Google Cloud Console
5. **Use environment variables** instead of hardcoding credentials
