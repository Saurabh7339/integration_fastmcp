import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/google/callback")
    
    # Google API Scopes
    GMAIL_SCOPE = os.getenv("GMAIL_SCOPE", "https://www.googleapis.com/auth/gmail.modify")
    GDRIVE_SCOPE = os.getenv("GDRIVE_SCOPE", "https://www.googleapis.com/auth/drive")
    GDOCS_SCOPE = os.getenv("GDOCS_SCOPE", "https://www.googleapis.com/auth/documents")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Combined scopes for OAuth
    SCOPES = [GMAIL_SCOPE, GDRIVE_SCOPE, GDOCS_SCOPE]
