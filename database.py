from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional
import os
import json
from config import Config

# Database configuration - Using PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5433/oneplace_core")

# Create engine - PostgreSQL configuration
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=300,    # Recycle connections every 5 minutes
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables"""
    SQLModel.metadata.create_all(engine)

def get_db_session() -> Session:
    """Get a database session"""
    return SessionLocal()

def get_workspace_by_id(workspace_id: str) -> Optional[dict]:
    """Get workspace by ID"""
    session = get_db_session()
    try:
        from models.workspace import Workspace
        workspace = session.get(Workspace, workspace_id)
        if workspace:
            return {
                "id": str(workspace.id),
                "name": workspace.name
            }
        return None
    finally:
        session.close()

def get_workspace_by_name(name: str) -> Optional[dict]:
    """Get workspace by name"""
    session = get_db_session()
    try:
        from models.workspace import Workspace
        workspace = session.query(Workspace).filter(Workspace.name == name).first()
        if workspace:
            print("testing the workspace",workspace)
            return {
                "id": str(workspace.id),
                "name": workspace.name
            }
        
        return None
    finally:
        session.close()

def create_workspace(name: str) -> Optional[dict]:
    """Create a new workspace using ORM approach"""
    session = get_db_session()
    try:
        from uuid import UUID
        from models.workspace import Workspace
        
        # Default UUIDs from existing database records
        default_org_id = UUID("c8306f9d-c97c-4ded-9a38-31f79eab656c")
        default_user_id = UUID("d1e7a429-402b-430e-8f7d-a168acca1a9a")
        default_llm_provider_id = UUID("2d6fd83e-5757-4887-ada7-b7ad247f117b")
        default_embedding_provider_id = UUID("d9aa74b6-3216-4d7f-9af6-8e4d540f83ff")
        default_llm_model_id = UUID("aee1ba0e-f272-40b3-be76-f470ece04952")
        default_embedding_model_id = UUID("b27f2676-b225-4bb4-b77d-9e1d27c40005")
        
        # Create workspace using ORM with all required fields
        workspace = Workspace(
            name=name,
            description="Default workspace description",
            default_llm_provider=default_llm_provider_id,
            default_embedding_provider=default_embedding_provider_id,
            default_embedding_model=default_embedding_model_id,
            default_llm_model=default_llm_model_id,
            is_active=True,
            is_public=False,
            organization_id=default_org_id,
            created_by_id=default_user_id
        )
        
        session.add(workspace)
        session.commit()
        session.refresh(workspace)
        
        return {
            "id": str(workspace.id),
            "name": workspace.name
        }
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_or_create_workspace(name: str) -> Optional[dict]:
    """Get or create a workspace for a username"""
    session = get_db_session()
    try:
        # Check if workspace exists
        existing_workspace = get_workspace_by_name(name)
        if existing_workspace:
            return existing_workspace
        return None
        
        # Create new workspace
        new_workspace = create_workspace(name)
        # return new_workspace
    finally:
        session.close()

def get_or_create_service_integration(service_type: str) -> Optional[dict]:
    """Get or create integration for a specific service"""
    session = get_db_session()
    try:
        from models.workspace import Integration
        
        service_name = f"Google {service_type.title()}"
        integration = session.query(Integration).filter(Integration.name == service_name).first()
        
        if not integration:
            # Set default ports for Google services
            default_ports = {
                "gmail": 993,  # IMAP SSL
                "drive": 443,  # HTTPS
                "docs": 443    # HTTPS
            }
            port = default_ports.get(service_type.lower(), None)
            
            integration = Integration(name=service_name, port=port)
            session.add(integration)
            session.commit()
            session.refresh(integration)
        
        return {
            "id": str(integration.id),
            "name": integration.name,
            "port": integration.port
        }
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_workspace_service_credentials(workspace_id: str, service_type: str) -> Optional[dict]:
    """Get credentials for a specific service in a workspace"""
    session = get_db_session()
    try:
        from models.workspace import WorkspaceIntegrationLink, Integration
        
        # Get service integration
        service_name = f"Google {service_type.title()}"
        service_integration = session.query(Integration).filter(Integration.name == service_name).first()
        if not service_integration:
            return None
        
        # Get workspace integration link
        link = session.query(WorkspaceIntegrationLink).filter(
            WorkspaceIntegrationLink.workspace_id == workspace_id,
            WorkspaceIntegrationLink.integration_id == service_integration.id
        ).first()
        
        if link and link.auth_details:
            # Handle both dict and JSON string for SQLite compatibility
            if isinstance(link.auth_details, str):
                try:
                    auth_details = json.loads(link.auth_details)
                except json.JSONDecodeError:
                    auth_details = {}
            else:
                auth_details = link.auth_details
                
            return {
                "workspace_id": str(link.workspace_id),
                "integration_id": str(link.integration_id),
                "service_type": service_type,
                "auth_details": auth_details,
                "created_date": link.created_date.isoformat() if link.created_date else None
            }
        return None
    finally:
        session.close()

def save_workspace_service_credentials(workspace_id: str, service_type: str, auth_details: dict) -> bool:
    """Save credentials for a specific service in a workspace"""
    session = get_db_session()
    try:
        from models.workspace import WorkspaceIntegrationLink, Integration
        
        # Get service integration
        service_name = f"Google {service_type.title()}"
        service_integration = session.query(Integration).filter(Integration.name == service_name).first()
        if not service_integration:
            service_integration = Integration(name=service_name)
            session.add(service_integration)
            session.commit()
            session.refresh(service_integration)
        
        # Check if link already exists
        link = session.query(WorkspaceIntegrationLink).filter(
            WorkspaceIntegrationLink.workspace_id == workspace_id,
            WorkspaceIntegrationLink.integration_id == service_integration.id
        ).first()
        
        if link:
            # Update existing link - serialize dict to JSON string for SQLite
            link.auth_details = json.dumps(auth_details)
        else:
            # Create new link - serialize dict to JSON string for SQLite
            link = WorkspaceIntegrationLink(
                workspace_id=workspace_id,
                integration_id=service_integration.id,
                auth_details=json.dumps(auth_details)
            )
            session.add(link)
        
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def remove_workspace_service_credentials(workspace_id: str, service_type: str) -> bool:
    """Remove credentials for a specific service in a workspace"""
    session = get_db_session()
    try:
        from models.workspace import WorkspaceIntegrationLink, Integration
        
        # Get service integration
        service_name = f"Google {service_type.title()}"
        service_integration = session.query(Integration).filter(Integration.name == service_name).first()
        if not service_integration:
            return False
        
        # Remove workspace integration link
        link = session.query(WorkspaceIntegrationLink).filter(
            WorkspaceIntegrationLink.workspace_id == workspace_id,
            WorkspaceIntegrationLink.integration_id == service_integration.id
        ).first()
        
        if link:
            session.delete(link)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_all_workspace_credentials(workspace_id: str) -> dict:
    """Get all service credentials for a workspace"""
    session = get_db_session()
    try:
        from models.workspace import WorkspaceIntegrationLink, Integration
        
        # Get all Google service integrations
        google_integrations = session.query(Integration).filter(
            Integration.name.like("Google %")
        ).all()
        
        credentials = {}
        for integration in google_integrations:
            # Extract service type from integration name
            service_type = integration.name.replace("Google ", "").lower()
            
            # Get credentials for this service
            link = session.query(WorkspaceIntegrationLink).filter(
                WorkspaceIntegrationLink.workspace_id == workspace_id,
                WorkspaceIntegrationLink.integration_id == integration.id
            ).first()
            
            if link and link.auth_details:
                # Parse JSON
                if isinstance(link.auth_details, str):
                    try:
                        auth_details = json.loads(link.auth_details)
                    except json.JSONDecodeError:
                        auth_details = {}
                else:
                    auth_details = link.auth_details
                
                credentials[service_type] = {
                    "has_credentials": True,
                    "integration_id": str(integration.id),
                    "created_date": link.created_date.isoformat() if link.created_date else None,
                    "auth_details": auth_details
                }
            else:
                credentials[service_type] = {
                    "has_credentials": False,
                    "integration_id": str(integration.id)
                }
        
        return credentials
    finally:
        session.close()
