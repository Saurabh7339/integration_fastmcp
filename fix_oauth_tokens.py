#!/usr/bin/env python3
"""
Script to fix OAuth token issues by clearing expired credentials.
"""

import sys
import os
from uuid import UUID
from database import get_db_session
from auth.oauth import GoogleOAuth

def clear_expired_credentials(workspace_id: str):
    """Clear expired credentials for a workspace"""
    try:
        workspace_uuid = UUID(workspace_id)
        session = get_db_session()
        
        print(f"Clearing expired credentials for workspace: {workspace_id}")
        
        # Clear credentials for all Google services
        services = ["gmail", "drive", "docs"]
        for service in services:
            try:
                oauth = GoogleOAuth(session, service)
                success = oauth.clear_all_credentials_for_workspace(workspace_uuid)
                if success:
                    print(f"✓ Cleared {service} credentials")
                else:
                    print(f"✗ Failed to clear {service} credentials")
            except Exception as e:
                print(f"✗ Error clearing {service} credentials: {e}")
        
        session.close()
        print("\n✓ Credential clearing complete!")
        print("You can now re-authenticate using the MCP tools.")
        
    except ValueError:
        print("✗ Invalid workspace_id format. Please provide a valid UUID.")
    except Exception as e:
        print(f"✗ Error: {e}")

def check_credentials_status(workspace_id: str):
    """Check the status of credentials for a workspace"""
    try:
        workspace_uuid = UUID(workspace_id)
        session = get_db_session()
        
        print(f"Checking credentials status for workspace: {workspace_id}")
        
        services = ["gmail", "drive", "docs"]
        for service in services:
            try:
                oauth = GoogleOAuth(session, service)
                status = oauth.get_workspace_credentials_status(workspace_uuid)
                print(f"\n{service.upper()} Status:")
                print(f"  Has credentials: {status.get('has_credentials', False)}")
                print(f"  Is valid: {status.get('is_valid', False)}")
                if status.get('error'):
                    print(f"  Error: {status['error']}")
            except Exception as e:
                print(f"✗ Error checking {service} credentials: {e}")
        
        session.close()
        
    except ValueError:
        print("✗ Invalid workspace_id format. Please provide a valid UUID.")
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    """Main function"""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 fix_oauth_tokens.py clear <workspace_id>")
        print("  python3 fix_oauth_tokens.py check <workspace_id>")
        print("\nExample:")
        print("  python3 fix_oauth_tokens.py clear 123e4567-e89b-12d3-a456-426614174000")
        return
    
    action = sys.argv[1].lower()
    workspace_id = sys.argv[2]
    
    if action == "clear":
        clear_expired_credentials(workspace_id)
    elif action == "check":
        check_credentials_status(workspace_id)
    else:
        print("✗ Invalid action. Use 'clear' or 'check'")

if __name__ == "__main__":
    main()
