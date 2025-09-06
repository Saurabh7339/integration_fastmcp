#!/usr/bin/env python3
"""
Simple test script to verify multiple client credential functionality.
This script tests the client credential selection logic without external dependencies.
"""

import os

def test_client_credentials_logic():
    """Test client credential selection logic"""
    
    print("Testing Multiple Client Credential Logic")
    print("=" * 50)
    
    # Simulate the Config.get_client_credentials logic
    def get_client_credentials(service_type: str) -> tuple[str, str]:
        """Simulate the client credential selection logic"""
        service_type = service_type.lower()
        
        # Simulate environment variables
        env_vars = {
            "gmail": ("GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET"),
            "drive": ("GDRIVE_CLIENT_ID", "GDRIVE_CLIENT_SECRET"),
            "docs": ("GDOCS_CLIENT_ID", "GDOCS_CLIENT_SECRET")
        }
        
        if service_type not in env_vars:
            raise ValueError(f"Unknown service type: {service_type}")
        
        client_id_var, client_secret_var = env_vars[service_type]
        client_id = os.getenv(client_id_var)
        client_secret = os.getenv(client_secret_var)
        
        # Fallback to generic credentials if service-specific ones are not set
        if not client_id or not client_secret:
            client_id = os.getenv("GOOGLE_CLIENT_ID")
            client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError(f"No OAuth credentials found for service '{service_type}'. "
                           f"Please set {client_id_var} and {client_secret_var} "
                           f"environment variables, or set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET as fallback.")
        
        return client_id, client_secret
    
    # Test cases
    test_cases = [
        ("gmail", "Gmail Service"),
        ("drive", "Google Drive Service"),
        ("docs", "Google Docs Service"),
        ("GMAIL", "Gmail Service (uppercase)"),
        ("DRIVE", "Google Drive Service (uppercase)"),
        ("DOCS", "Google Docs Service (uppercase)")
    ]
    
    for service_type, description in test_cases:
        print(f"\nTesting {description} ({service_type}):")
        try:
            client_id, client_secret = get_client_credentials(service_type)
            print(f"  ✓ Success: Client ID = {client_id[:20]}..." if client_id else "  ✗ No Client ID")
            print(f"  ✓ Success: Client Secret = {'*' * 20}..." if client_secret else "  ✗ No Client Secret")
        except ValueError as e:
            print(f"  ✗ Error: {e}")
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
    
    # Test invalid service type
    print(f"\nTesting Invalid Service Type:")
    try:
        client_id, client_secret = get_client_credentials("invalid_service")
        print(f"  ✗ Should have failed but got: {client_id}")
    except ValueError as e:
        print(f"  ✓ Expected error: {e}")
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
    
    print("\n" + "=" * 50)
    print("Environment Variables Check:")
    print("=" * 50)
    
    # Check which environment variables are set
    env_vars = [
        "GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET",
        "GDRIVE_CLIENT_ID", "GDRIVE_CLIENT_SECRET", 
        "GDOCS_CLIENT_ID", "GDOCS_CLIENT_SECRET",
        "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        status = "✓ Set" if value else "✗ Not Set"
        print(f"  {var}: {status}")
    
    print("\nRecommendations:")
    print("- Set service-specific credentials (GMAIL_CLIENT_ID, etc.) for better security")
    print("- Or set fallback credentials (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)")
    print("- See env.example for configuration examples")

if __name__ == "__main__":
    test_client_credentials_logic()
