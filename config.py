import os

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, use environment variables directly
    pass

class Config:
    # Google OAuth Configuration - Multiple Client Support
    # Gmail OAuth Credentials
    GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
    GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
    
    # Google Drive OAuth Credentials
    GDRIVE_CLIENT_ID = os.getenv("GDRIVE_CLIENT_ID")
    GDRIVE_CLIENT_SECRET = os.getenv("GDRIVE_CLIENT_SECRET")
    
    # Google Docs OAuth Credentials
    GDOCS_CLIENT_ID = os.getenv("GDOCS_CLIENT_ID")
    GDOCS_CLIENT_SECRET = os.getenv("GDOCS_CLIENT_SECRET")
    
    # Fallback to generic credentials if service-specific ones are not set
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://oneplace-api.speakmulti.com/api/google/callback")
    
    # Google API Scopes
    GMAIL_SCOPE = os.getenv("GMAIL_SCOPE", "https://www.googleapis.com/auth/gmail.modify")
    GDRIVE_SCOPE = os.getenv("GDRIVE_SCOPE", "https://www.googleapis.com/auth/drive")
    GDOCS_SCOPE = os.getenv("GDOCS_SCOPE", "https://www.googleapis.com/auth/documents")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5433/oneplace_core")
    
    # Combined scopes for OAuth
    SCOPES = [GMAIL_SCOPE, GDRIVE_SCOPE, GDOCS_SCOPE]
    
    @classmethod
    def get_client_credentials(cls, service_type: str):
        """
        Get client_id and client_secret for a specific service type.
        
        Args:
            service_type: The service type ('gmail', 'drive', 'docs')
            
        Returns:
            tuple of (client_id, client_secret)
            
        Raises:
            ValueError: If no credentials are found for the service
        """
        service_type = service_type.lower()
        
        if service_type == "gmail":
            client_id = cls.GMAIL_CLIENT_ID
            client_secret = cls.GMAIL_CLIENT_SECRET
        elif service_type == "drive":
            client_id = cls.GDRIVE_CLIENT_ID
            client_secret = cls.GDRIVE_CLIENT_SECRET
        elif service_type == "docs":
            client_id = cls.GDOCS_CLIENT_ID
            client_secret = cls.GDOCS_CLIENT_SECRET
        else:
            raise ValueError(f"Unknown service type: {service_type}")
        
        # Fallback to generic credentials if service-specific ones are not set
        if not client_id or not client_secret:
            client_id = cls.GOOGLE_CLIENT_ID
            client_secret = cls.GOOGLE_CLIENT_SECRET
        
        if not client_id or not client_secret:
            raise ValueError(f"No OAuth credentials found for service '{service_type}'. "
                           f"Please set {service_type.upper()}_CLIENT_ID and {service_type.upper()}_CLIENT_SECRET "
                           f"environment variables, or set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET as fallback.")
        
        return client_id, client_secret
