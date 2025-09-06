#!/usr/bin/env python3
"""
Utility script to clear Google OAuth credentials when scope changes occur.
This helps resolve the "Scope has changed" error from Google OAuth.
"""

import sys
import os
from uuid import UUID
from sqlmodel import create_engine, Session, select
from models.workspace import Workspace, WorkspaceIntegrationLink

def clear_credentials_for_workspace(workspace_id: str, db_url: str = "sqlite:///test.db"):
    """Clear all Google service credentials for a workspace"""
    try:
        # Create database connection
        engine = create_engine(db_url)
        session = Session(engine)
        
        # Convert string to UUID
        workspace_uuid = UUID(workspace_id)
        
        # Find all Google service integrations for this workspace
        stmt = select(WorkspaceIntegrationLink).where(
            WorkspaceIntegrationLink.workspace_id == workspace_uuid
        )
        links = session.execute(stmt).scalars().all()
        
        if not links:
            print(f"No credentials found for workspace {workspace_id}")
            return True
        
        # Remove all Google service credentials
        removed_count = 0
        for link in links:
            if link.integration.name.startswith("Google"):
                print(f"Removing credentials for: {link.integration.name}")
                session.delete(link)
                removed_count += 1
        
        session.commit()
        session.close()
        
        print(f"Successfully cleared {removed_count} Google service credentials for workspace {workspace_id}")
        print("You can now re-authorize with the new scopes.")
        return True
        
    except Exception as e:
        print(f"Error clearing credentials: {e}")
        return False

def list_workspaces(db_url: str = "sqlite:///test.db"):
    """List all workspaces in the database"""
    try:
        engine = create_engine(db_url)
        session = Session(engine)
        
        stmt = select(Workspace)
        workspaces = session.execute(stmt).scalars().all()
        
        if not workspaces:
            print("No workspaces found in database")
            return
        
        print("Available workspaces:")
        for workspace in workspaces:
            print(f"  - ID: {workspace.id}, Name: {workspace.name}")
        
        session.close()
        
    except Exception as e:
        print(f"Error listing workspaces: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python clear_credentials.py list                    # List all workspaces")
        print("  python clear_credentials.py clear <workspace_id>    # Clear credentials for workspace")
        print("  python clear_credentials.py clear-all               # Clear all credentials")
        return
    
    command = sys.argv[1]
    db_url = os.getenv("DATABASE_URL", "sqlite:///test.db")
    
    if command == "list":
        list_workspaces(db_url)
    elif command == "clear":
        if len(sys.argv) < 3:
            print("Error: Please provide workspace ID")
            return
        workspace_id = sys.argv[2]
        clear_credentials_for_workspace(workspace_id, db_url)
    elif command == "clear-all":
        try:
            engine = create_engine(db_url)
            session = Session(engine)
            
            # Remove all Google service credentials
            stmt = select(WorkspaceIntegrationLink)
            links = session.execute(stmt).scalars().all()
            
            removed_count = 0
            for link in links:
                if link.integration.name.startswith("Google"):
                    session.delete(link)
                    removed_count += 1
            
            session.commit()
            session.close()
            
            print(f"Successfully cleared {removed_count} Google service credentials")
            print("You can now re-authorize with the new scopes.")
            
        except Exception as e:
            print(f"Error clearing all credentials: {e}")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
