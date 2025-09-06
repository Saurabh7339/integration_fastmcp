#!/usr/bin/env python3
"""
Main API server for Google Services MCP OAuth Integration
Provides end-to-end OAuth flow through REST APIs
"""

import traceback
from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import uvicorn
import json
import base64
from uuid import UUID

# Import our existing modules
from auth.oauth import GoogleOAuth
from database import (
    create_tables, get_db_session, create_workspace, 
    get_workspace_by_name, get_or_create_workspace,
    get_workspace_service_credentials, save_workspace_service_credentials
)
from config import Config

# Create FastAPI app
app = FastAPI(
    title="Google Services MCP - OAuth Integration API",
    description="Complete OAuth integration for Google Services (Gmail, Drive, Docs)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Pydantic models for API requests/responses
class WorkspaceCreate(BaseModel):
    name: str

class OAuthInitiateRequest(BaseModel):
    workspace_id: UUID
    service: str  # gmail, drive, or docs

class OAuthCallbackRequest(BaseModel):
    code: str
    state: Optional[str] = None

class ServiceTestRequest(BaseModel):
    username: str
    service: str

class WorkspaceResponse(BaseModel):
    id: str
    name: str
    status: str

class OAuthStatusResponse(BaseModel):
    workspace_id: str
    username: str
    service: str
    is_authenticated: bool
    last_authenticated: Optional[str] = None

class ServiceCredentialsResponse(BaseModel):
    workspace_id: str
    service: str
    is_valid: bool
    expires_at: Optional[str] = None

# Service types
SERVICES = ["gmail", "drive", "docs"]

# Utility functions
def encode_state(username: str, service: str) -> str:
    """Encode username and service in state parameter"""
    state_data = {"username": username, "service": service}
    state_json = json.dumps(state_data)
    return base64.b64encode(state_json.encode()).decode()

def decode_state(state: str) -> dict:
    """Decode state parameter to get username and service"""
    try:
        state_json = base64.b64decode(state.encode()).decode()
        return json.loads(state_json)
    except:
        return {"username": "default", "service": "unknown"}

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Google Services MCP OAuth Integration API",
        "version": "1.0.0",
        "available_services": SERVICES,
        "endpoints": {
            "workspace": "/api/workspace",
            "oauth_initiate": "/api/oauth/initiate",
            "oauth_callback": "/api/oauth/callback",
            "oauth_status": "/api/oauth/status",
            "service_test": "/api/service/test"
        }
    }

# Workspace Management APIs
@app.post("/api/workspace", response_model=WorkspaceResponse)
async def create_workspace_api(request: WorkspaceCreate):
    """Create a new workspace for a user"""
    try:
        workspace = get_or_create_workspace(request.name)
        return WorkspaceResponse(
            id=workspace["id"],
            name=workspace["name"],
            status="created"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workspace/{username}", response_model=WorkspaceResponse)
async def get_workspace_api(username: str):
    """Get workspace information for a user"""
    try:
        workspace = get_workspace_by_name(username)
        if not workspace:
            raise HTTPException(status_code=404, detail="Workspace not found")
        
        return WorkspaceResponse(
            id=workspace["id"],
            name=workspace["name"],
            status="exists"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# OAuth Integration APIs
@app.post("/api/oauth/initiate")
async def oauth_initiate(request: OAuthInitiateRequest):
    """Initiate OAuth flow for a specific service"""
    try:
        # Validate service
        if request.service not in SERVICES:
            raise HTTPException(status_code=400, detail=f"Invalid service. Must be one of: {SERVICES}")
        
        # Get or create workspace
        workspace = get_or_create_workspace(request.workspace_id)
        if workspace is None:
            raise HTTPException(status_code=400, detail="Workspace not found")
        
        # Initialize OAuth for the specific service
        db_session = get_db_session()
        try:
            oauth = GoogleOAuth(db_session, request.service)
            
            # Get the authorization URL with username and service encoded in state
            auth_url = oauth.get_authorization_url(username=str(request.workspace_id), service=request.service)
            
            # Create redirect URL for easy OAuth flow
            redirect_url = f"/oauth/redirect?authorization_url={auth_url.replace('&', '%26')}"
            
            return {
                "success": True,
                "workspace_id": workspace["id"],
                "username": str(request.workspace_id),
                "service": request.service,
                "authorization_url": auth_url,
                "redirect_url": redirect_url,
                "state": encode_state(str(request.workspace_id), request.service),
                "message": f"OAuth flow initiated for {request.service}"
            }
        finally:
            db_session.close()
            
    except HTTPException:
        traceback.print_exc()
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/google/callback")
async def oauth_callback(
    code: str = Query(...),
    state: Optional[str] = Query(None)
):
    """Handle OAuth callback and exchange code for tokens"""
    try:
        # Decode state parameter to get username and service
        if state:
            state_data = decode_state(state)
            username_from_state = state_data.get("username", "default")
            service_from_state = state_data.get("service", "unknown")
        else:
            raise HTTPException(status_code=400, detail="Missing state parameter")
        
        if service_from_state not in SERVICES:
            raise HTTPException(status_code=400, detail=f"Invalid service: {service_from_state}")
        
        # Get or create workspace
        workspace = get_or_create_workspace(username_from_state)
        
        # Initialize OAuth for the specific service
        db_session = get_db_session()
        try:
            oauth = GoogleOAuth(db_session, service_from_state)
            tokens = oauth.exchange_code_for_tokens(code, UUID(workspace["id"]))
            
            # return {
            #     "success": True,
            #     "workspace_id": workspace["id"],
            #     "username": username_from_state,
            #     "service": service_from_state,
            #     "message": f"Successfully authenticated with {service_from_state}",
            #     "tokens_received": bool(tokens and not tokens.get("error")),
            #     "redirect_url": f"/oauth-success?service={service_from_state}&username={username_from_state}"
            # }
            return RedirectResponse(url="https://app.speakmulti.com")
            
        finally:
            db_session.close()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/oauth/status/{username}/{service}", response_model=OAuthStatusResponse)
async def oauth_status(username: str, service: str):
    """Get OAuth status for a specific user and service"""
    try:
        if service not in SERVICES:
            raise HTTPException(status_code=400, detail=f"Invalid service. Must be one of: {SERVICES}")
        
        # Get workspace
        workspace = get_workspace_by_name(username)
        if not workspace:
            raise HTTPException(status_code=404, detail="Workspace not found")
        
        # Check OAuth status
        db_session = get_db_session()
        try:
            oauth = GoogleOAuth(db_session, service)
            status = oauth.get_workspace_credentials_status(UUID(workspace["id"]))
            
            return OAuthStatusResponse(
                workspace_id=workspace["id"],
                username=username,
                service=service,
                is_authenticated=status.get("is_authenticated", False),
                last_authenticated=status.get("last_authenticated")
            )
        finally:
            db_session.close()
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/oauth/status/{username}")
async def oauth_status_all(username: str):
    """Get OAuth status for all services for a specific user"""
    try:
        # Get workspace
        workspace = get_workspace_by_name(username)
        if not workspace:
            raise HTTPException(status_code=404, detail="Workspace not found")
        
        # Check OAuth status for all services
        db_session = get_db_session()
        try:
            all_status = {}
            for service in SERVICES:
                oauth = GoogleOAuth(db_session, service)
                status = oauth.get_workspace_credentials_status(UUID(workspace["id"]))
                all_status[service] = status
            
            return {
                "workspace_id": workspace["id"],
                "username": username,
                "services_status": all_status
            }
        finally:
            db_session.close()
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Service Testing APIs
@app.post("/api/service/test")
async def test_service(request: ServiceTestRequest):
    """Test a specific service functionality"""
    try:
        if request.service not in SERVICES:
            raise HTTPException(status_code=400, detail=f"Invalid service. Must be one of: {SERVICES}")
        
        # Get workspace
        workspace = get_workspace_by_name(request.username)
        if not workspace:
            raise HTTPException(status_code=404, detail="Workspace not found")
        
        # Initialize OAuth for the specific service
        db_session = get_db_session()
        try:
            oauth = GoogleOAuth(db_session, request.service)
            creds = oauth.get_valid_credentials(UUID(workspace["id"]))
            
            if not creds:
                raise HTTPException(
                    status_code=401, 
                    detail=f"No valid {request.service} credentials found. Please authenticate first."
                )
            
            # Test the service based on type
            if request.service == "gmail":
                from services.gmail_service import GmailService
                service_instance = GmailService(creds)
                result = service_instance.read_inbox(max_results=5)
                
            elif request.service == "drive":
                from services.gdrive_service import GoogleDriveService
                service_instance = GoogleDriveService(creds)
                result = service_instance.list_files(max_results=5)
                
            elif request.service == "docs":
                from services.gdocs_service import GoogleDocsService
                service_instance = GoogleDocsService(creds)
                result = service_instance.list_documents(max_results=5)
            
            return {
                "success": True,
                "workspace_id": workspace["id"],
                "username": request.username,
                "service": request.service,
                "test_result": result,
                "message": f"Service {request.service} tested successfully"
            }
            
        finally:
            db_session.close()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health Check API
@app.get("/oauth/redirect")
async def oauth_redirect(authorization_url: str = Query(...)):
    """Redirect to OAuth authorization URL"""
    try:
        # Validate that the URL is a Google OAuth URL for security
        if not authorization_url.startswith("https://accounts.google.com/o/oauth2/auth"):
            raise HTTPException(status_code=400, detail="Invalid authorization URL")
        
        return RedirectResponse(url=authorization_url)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db_session = get_db_session()
        db_session.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "services": SERVICES,
            "timestamp": "2025-09-04T20:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "detail": "The requested resource was not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    print("🚀 Starting Google Services MCP OAuth Integration API...")
    print("📊 Database tables will be created/verified on startup")
    print("🌐 API will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔐 Available services:", ", ".join(SERVICES))
    
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True,
        log_level="info"
    )
