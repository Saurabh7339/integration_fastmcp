#!/usr/bin/env python3
"""
Setup integration ports in the database.
This script creates or updates the Integration table with port configurations for Google services.
"""

import os
import sys
from database import get_db_session, create_tables
from config import Config
from models.workspace import Integration
from sqlmodel import select

def setup_integration_ports():
    """Setup port configurations for integrations"""
    print("Setting up Integration Ports")
    print("=" * 30)
    
    # Create database tables
    try:
        create_tables()
        print("✓ Database tables created/verified")
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        return
    
    session = get_db_session()
    
    try:
        # Define service configurations
        services = [
            {"name": "gmail", "port": 8001, "description": "Gmail MCP Server"},
            {"name": "drive", "port": 8002, "description": "Google Drive MCP Server"},
            {"name": "docs", "port": 8003, "description": "Google Docs MCP Server"}
        ]
        
        for service_config in services:
            service_name = service_config["name"]
            port = service_config["port"]
            description = service_config["description"]
            
            # Check if integration exists
            stmt = select(Integration).where(Integration.name == service_name)
            integration = session.execute(stmt).scalar_one_or_none()
            
            if integration:
                # Update existing integration
                if integration.port != port:
                    integration.port = port
                    session.commit()
                    print(f"✓ Updated {service_name} integration: Port {port}")
                else:
                    print(f"✓ {service_name} integration already configured: Port {port}")
            else:
                # Create new integration
                integration = Integration(name=service_name, port=port)
                session.add(integration)
                session.commit()
                print(f"✓ Created {service_name} integration: Port {port}")
        
        # Display current configuration
        print("\nCurrent Integration Configuration:")
        print("-" * 40)
        
        stmt = select(Integration)
        integrations = session.execute(stmt).scalars().all()
        
        for integration in integrations:
            print(f"  {integration.name}: Port {integration.port}")
        
        print("\n✓ Integration ports setup complete!")
        
    except Exception as e:
        print(f"✗ Error setting up integration ports: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    """Main function"""
    setup_integration_ports()

if __name__ == "__main__":
    main()
