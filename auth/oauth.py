import os
import json
from typing import Dict, Any, Optional
from uuid import UUID
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from sqlmodel import Session, select

# Import your models (you'll need to adjust the import path)
from models.workspace import Workspace, Integration, WorkspaceIntegrationLink

class GoogleOAuth:
    def __init__(self, db_session: Session, service_type: str):
        self.db_session = db_session
        self.service_type = service_type
        self.scopes =  self._get_scopes_for_service(service_type)
        
        # Get or create service integration
        self.service_integration = self._get_or_create_service_integration(service_type)
        
        # OAuth configuration - Get service-specific credentials
        from config import Config
        self.client_id, self.client_secret = Config.get_client_credentials(service_type)
        # Use the exact callback route that matches our web interface
        self.redirect_uri = Config.GOOGLE_REDIRECT_URI

        print(f"OAuth configuration - Client ID: {self.client_id}, Client Secret: {self.client_secret}, Redirect URI: {self.redirect_uri}")
    
    def _get_scopes_for_service(self, service_type: str) -> list:
        """Get the appropriate scopes for a specific service"""
        scope_map = {
            "gmail": ["https://www.googleapis.com/auth/gmail.modify"],
            "drive": ["https://www.googleapis.com/auth/drive"],
            "docs": ["https://www.googleapis.com/auth/documents"]
        }
        return scope_map.get(service_type, [])
    
    def _get_or_create_service_integration(self, service_type: str):
        """Get or create integration for a specific service"""
        from models.workspace import Integration
        
        service_name = f"{service_type}"
        
        # Use SQLAlchemy query instead of SQLModel exec
        stmt = select(Integration).where(Integration.name == service_name)
        result = self.db_session.execute(stmt).scalar_one_or_none()
        
        if not result:
            integration = Integration(name=service_name)
            self.db_session.add(integration)
            self.db_session.commit()
            self.db_session.refresh(integration)
            return integration
        
        return result
    
    def get_authorization_url(self, username: str = None, service: str = None) -> str:
        """Generate Google OAuth authorization URL"""
        # Create OAuth client configuration
        client_config = {
            "web": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [self.redirect_uri],
                "scopes": self.scopes
            }
        }
        
        # Create flow with proper configuration
        flow = Flow.from_client_config(
            client_config,
            scopes=self.scopes
        )
        
        # Set redirect URI
        flow.redirect_uri = self.redirect_uri
        
        # Generate authorization URL with proper parameters
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # If username and service are provided, encode them in the state
        if username and service:
            import base64
            import json
            state_data = {"username": username, "service": service}
            state_json = json.dumps(state_data)
            encoded_state = base64.b64encode(state_json.encode()).decode()
            # Replace the Google-generated state with our encoded one
            authorization_url = authorization_url.replace(f"state={state}", f"state={encoded_state}")
        
        return authorization_url
    
    def exchange_code_for_tokens(self, authorization_code: str, workspace_id: UUID) -> Dict[str, Any]:
        """Exchange authorization code for access and refresh tokens"""
        # Create OAuth client configuration
        client_config = {
            "web": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [self.redirect_uri],
                "scopes": self.scopes
            }
        }
        
        # Create flow with proper configuration
        flow = Flow.from_client_config(
            client_config,
            scopes=self.scopes
        )
        
        # Set redirect URI
        flow.redirect_uri = self.redirect_uri
        
        # Exchange code for tokens
        flow.fetch_token(code=authorization_code)
        
        # Get credentials
        credentials = flow.credentials
        
        # Save credentials to database
        self._save_credentials(workspace_id, credentials)
        
        return {
            "success": True,
            "service_type": self.service_type,
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "expires_at": credentials.expiry.isoformat() if credentials.expiry else None
        }
    
    def get_valid_credentials(self, workspace_id: UUID) -> Optional[Credentials]:
        """Get valid credentials for a workspace, refreshing if necessary"""
        from models.workspace import WorkspaceIntegrationLink
        
        # Get credentials from database
        stmt = select(WorkspaceIntegrationLink).where(
            WorkspaceIntegrationLink.workspace_id == workspace_id,
            WorkspaceIntegrationLink.integration_id == self.service_integration.id
        )
        link = self.db_session.execute(stmt).scalar_one_or_none()
        
        if not link or not link.auth_details:
            return None
        
        # Parse auth_details (handle both dict and JSON string for SQLite)
        if isinstance(link.auth_details, str):
            try:
                auth_details = json.loads(link.auth_details)
            except json.JSONDecodeError:
                return None
        else:
            auth_details = link.auth_details
        
        # Check if stored scopes match current scopes
        stored_scopes = auth_details.get('scopes', [])
        if set(stored_scopes) != set(self.scopes):
            # Scopes have changed, need to re-authorize
            print(f"Scope mismatch detected. Stored: {stored_scopes}, Current: {self.scopes}")
            print("Clearing existing credentials. Re-authorization required.")
            self._remove_credentials(workspace_id)
            return None
        
        # Create credentials object
        credentials = Credentials(
            token=auth_details.get('token'),
            refresh_token=auth_details.get('refresh_token'),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=self.scopes
        )
        
        # Check if token is expired and refresh if necessary
        if credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                # Save refreshed credentials
                self._save_credentials(workspace_id, credentials)
            except RefreshError:
                # Refresh failed, remove invalid credentials
                self._remove_credentials(workspace_id)
                return None
        
        return credentials
    
    def _save_credentials(self, workspace_id: UUID, credentials: Credentials):
        """Save credentials to database"""
        from models.workspace import WorkspaceIntegrationLink
        
        # Prepare credentials data
        creds_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'expiry': credentials.expiry.isoformat() if credentials.expiry else None,
            'scopes': credentials.scopes
        }
        
        # Check if link already exists
        stmt = select(WorkspaceIntegrationLink).where(
            WorkspaceIntegrationLink.workspace_id == workspace_id,
            WorkspaceIntegrationLink.integration_id == self.service_integration.id
        )
        link = self.db_session.execute(stmt).scalar_one_or_none()
        
        if link:
            # Update existing link - serialize dict to JSON string for SQLite
            link.auth_details = json.dumps(creds_data)
        else:
            # Create new link - serialize dict to JSON string for SQLite
            link = WorkspaceIntegrationLink(
                workspace_id=workspace_id,
                integration_id=self.service_integration.id,
                auth_details=json.dumps(creds_data)
            )
            self.db_session.add(link)
        
        self.db_session.commit()
    
    def _remove_credentials(self, workspace_id: UUID):
        """Remove credentials from database"""
        from models.workspace import WorkspaceIntegrationLink
        
        stmt = select(WorkspaceIntegrationLink).where(
            WorkspaceIntegrationLink.workspace_id == workspace_id,
            WorkspaceIntegrationLink.integration_id == self.service_integration.id
        )
        link = self.db_session.execute(stmt).scalar_one_or_none()
        
        if link:
            self.db_session.delete(link)
            self.db_session.commit()
    
    def revoke_credentials(self, workspace_id: UUID) -> bool:
        """Revoke and remove credentials for a workspace"""
        try:
            # Get current credentials
            credentials = self.get_valid_credentials(workspace_id)
            
            if credentials:
                # Revoke with Google
                try:
                    credentials.revoke(Request())
                except Exception:
                    # Continue even if Google revocation fails
                    pass
            
            # Remove from database
            self._remove_credentials(workspace_id)
            return True
            
        except Exception:
            return False
    
    def clear_all_credentials_for_workspace(self, workspace_id: UUID) -> bool:
        """Clear all Google service credentials for a workspace (useful for scope changes)"""
        try:
            from models.workspace import WorkspaceIntegrationLink
            
            # Find all Google service integrations for this workspace
            stmt = select(WorkspaceIntegrationLink).where(
                WorkspaceIntegrationLink.workspace_id == workspace_id
            )
            links = self.db_session.execute(stmt).scalars().all()
            
            # Remove all Google service credentials
            for link in links:
                if link.integration.name.startswith("Google"):
                    self.db_session.delete(link)
            
            self.db_session.commit()
            return True
            
        except Exception as e:
            print(f"Error clearing credentials: {e}")
            return False
    
    def get_workspace_credentials_status(self, workspace_id: UUID) -> Dict[str, Any]:
        """Get the status of credentials for a workspace"""
        from models.workspace import WorkspaceIntegrationLink
        
        stmt = select(WorkspaceIntegrationLink).where(
            WorkspaceIntegrationLink.workspace_id == workspace_id,
            WorkspaceIntegrationLink.integration_id == self.service_integration.id
        )
        link = self.db_session.execute(stmt).scalar_one_or_none()
        
        if link and link.auth_details:
            # Parse auth_details
            if isinstance(link.auth_details, str):
                try:
                    auth_details = json.loads(link.auth_details)
                except json.JSONDecodeError:
                    auth_details = {}
            else:
                auth_details = link.auth_details
            
            return {
                "has_credentials": True,
                "service_type": self.service_type,
                "integration_id": str(self.service_integration.id),
                "integration_name": self.service_integration.name,
                "created_date": link.created_date.isoformat() if link.created_date else None,
                "scopes": auth_details.get('scopes', []),
                "expires_at": auth_details.get('expiry')
            }
        else:
            return {
                "has_credentials": False,
                "service_type": self.service_type,
                "integration_id": str(self.service_integration.id),
                "integration_name": self.service_integration.name
            }
