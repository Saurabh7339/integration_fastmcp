from fastapi import FastAPI, Request, Form, HTTPException
from fastapi import Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from auth.oauth import GoogleOAuth
from database import create_tables, get_db_session, create_workspace, get_workspace_by_name
from config import Config
from uuid import UUID
from typing import Optional
import json
import base64

app = FastAPI(title="Google Services MCP - Web Interface")
templates = Jinja2Templates(directory="templates")

# Create database tables on startup
create_tables()

# Service types for OAuth
SERVICES = ["gmail", "drive", "docs"]

def get_or_create_workspace(username: str):
    """Get or create a workspace for a username"""
    session = get_db_session()
    try:
        # Check if workspace exists
        existing_workspace = get_workspace_by_name(username)
        if existing_workspace:
            return existing_workspace
        
        # Create new workspace
        new_workspace = create_workspace(username)
        return new_workspace
    finally:
        session.close()

def get_workspace_credentials_status(username: str):
    """Get the status of all service credentials for a workspace"""
    session = get_db_session()
    try:
        workspace = get_workspace_by_name(username)
        if not workspace:
            return {}
        
        # Initialize OAuth for each service to check credentials
        credentials_status = {}
        for service_type in SERVICES:
            oauth = GoogleOAuth(session, service_type)
            status = oauth.get_workspace_credentials_status(UUID(workspace["id"]))
            credentials_status[service_type] = status
        
        return credentials_status
    finally:
        session.close()

def encode_state(username: str, service: str) -> str:
    """Encode username and service in state parameter"""
    state_data = {"username": username, "service": service}
    state_json = json.dumps(state_data)
    # Use standard base64 encoding
    return base64.b64encode(state_json.encode()).decode()

def decode_state(state: str) -> dict:
    """Decode state parameter to get username and service"""
    try:
        # Use standard base64 decoding
        state_json = base64.b64decode(state.encode()).decode()
        return json.loads(state_json)
    except:
        return {"username": "default", "service": "unknown"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with service selection and username input"""
    return templates.TemplateResponse("home.html", {"request": request, "services": SERVICES})

@app.get("/auth/{service}", response_class=HTMLResponse)
async def auth_page(request: Request, service: str, username: str):
    """OAuth authorization page for a specific service"""
    if service not in SERVICES:
        raise HTTPException(status_code=400, detail="Invalid service")
    
    # Get or create workspace for username
    workspace = get_or_create_workspace(username)
    
    # Initialize OAuth for the specific service
    db_session = get_db_session()
    try:
        oauth = GoogleOAuth(db_session, service)
        # Get the authorization URL with username and service encoded in state
        auth_url = oauth.get_authorization_url(username=username, service=service)
        
        return templates.TemplateResponse("auth.html", {
            "request": request, 
            "auth_url": auth_url, 
            "service": service, 
            "username": username,
            "workspace_id": workspace["id"]
        })
    finally:
        db_session.close()

@app.get("/google/callback")
async def oauth_callback(
    code: str = Query(...),
    state: Optional[str] = Query(None),
    # username: Optional[str] = Query(None),
    # service: Optional[str] = Query(None),
):
    """OAuth callback handler - unique path to avoid conflicts"""
    try:
        # Decode state parameter to get username and service
        if state:
            state_data = decode_state(state)
            username_from_state = state_data.get("username", "default")
            service_from_state = state_data.get("service", "unknown")
        else:
            username_from_state = "default"
            service_from_state = "unknown"
        
        # Prefer values from state; fall back to query if provided
        final_username = username_from_state or username or "default"
        final_service = service_from_state or service or "unknown"
        
        if final_service not in SERVICES:
            return RedirectResponse(url=f"/success?success=false&service={final_service}&username={final_username}&error=Invalid service")
        
        # Get or create workspace
        workspace = get_or_create_workspace(final_username)
        
        # Initialize OAuth for the specific service
        db_session = get_db_session()
        try:
            oauth = GoogleOAuth(db_session, final_service)
            tokens = oauth.exchange_code_for_tokens(code, UUID(workspace["id"]))
            
            # Redirect to success page
            return RedirectResponse(url=f"/success?success=true&service={final_service}&username={final_username}")
            
        finally:
            db_session.close()
        
    except Exception as e:
        return str(e)

@app.get("/success", response_class=HTMLResponse)
async def success_page(request: Request, success: bool, service: str = None, username: str = None, error: str = None):
    """Success/failure page after OAuth"""
    return templates.TemplateResponse("success.html", {
        "request": request, 
        "success": success, 
        "service": service,
        "username": username, 
        "error": error
    })

@app.get("/dashboard/{username}", response_class=HTMLResponse)
async def dashboard(request: Request, username: str):
    """Dashboard showing all service credentials and status"""
    # Get workspace credentials status
    credentials_status = get_workspace_credentials_status(username)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "username": username,
        "services": SERVICES,
        "credentials_status": credentials_status
    })

@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    """Test page for MCP tools"""
    return templates.TemplateResponse("test.html", {"request": request, "services": SERVICES})

@app.post("/test/{service}")
async def test_service(service: str, username: str = Form(...)):
    """Test a specific service functionality"""
    if service not in SERVICES:
        raise HTTPException(status_code=400, detail="Invalid service")
    
    try:
        # Get workspace
        workspace = get_or_create_workspace(username)
        
        # Initialize OAuth for the specific service
        db_session = get_db_session()
        try:
            oauth = GoogleOAuth(db_session, service)
            creds = oauth.get_valid_credentials(UUID(workspace["id"]))
            
            if not creds:
                raise HTTPException(status_code=401, detail=f"No valid {service} credentials found")
            
            # Test the service based on type
            if service == "gmail":
                from services.gmail_service import GmailService
                service_instance = GmailService(creds)
                result = service_instance.read_inbox(max_results=5)
                
            elif service == "drive":
                from services.gdrive_service import GoogleDriveService
                service_instance = GoogleDriveService(creds)
                result = service_instance.list_files(page_size=5)
                
            elif service == "docs":
                from services.gdocs_service import GoogleDocsService
                service_instance = GoogleDocsService(creds)
                result = service_instance.list_documents(page_size=5)
            
            return {"success": True, "service": service, "result": result}
            
        finally:
            db_session.close()
        
    except Exception as e:
        return {"success": False, "service": service, "error": str(e)}

@app.get("/api/credentials/{username}")
async def get_credentials_api(username: str):
    """API endpoint to get credentials status for a username"""
    try:
        credentials_status = get_workspace_credentials_status(username)
        return {"success": True, "username": username, "credentials": credentials_status}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/revoke/{service}")
async def revoke_credentials(service: str, username: str = Form(...)):
    """Revoke credentials for a specific service"""
    if service not in SERVICES:
        raise HTTPException(status_code=400, detail="Invalid service")
    
    try:
        workspace = get_or_create_workspace(username)
        db_session = get_db_session()
        
        try:
            oauth = GoogleOAuth(db_session, service)
            oauth.revoke_credentials(UUID(workspace["id"]))
            return {"success": True, "message": f"{service} credentials revoked successfully"}
        finally:
            db_session.close()
            
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/workspaces")
async def list_workspaces():
    """List all workspaces (for admin purposes)"""
    try:
        db_session = get_db_session()
        try:
            from models.workspace import Workspace
            workspaces = db_session.query(Workspace).all()
            return {
                "success": True,
                "workspaces": [
                    {"id": str(w.id), "name": w.name} for w in workspaces
                ]
            }
        finally:
            db_session.close()
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("🚀 Starting Google Services MCP Web Interface...")
    print("📊 Database tables created/verified")
    print(f"🌐 Server will run on {Config.HOST}:{Config.PORT}")
    print("🔐 Available services:", ", ".join(SERVICES))
    print("⚠️  Make sure to set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables")
    print("⚠️  IMPORTANT: Configure Google OAuth app with redirect URI: http://localhost:8000/auth/callback")
    uvicorn.run(app, host=Config.HOST, port=8022)
