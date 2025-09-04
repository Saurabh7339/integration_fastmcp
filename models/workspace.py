from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, TypeDecorator
from sqlalchemy.types import String as SQLString

class SQLiteUUID(TypeDecorator):
    """Custom UUID type for SQLite compatibility"""
    impl = SQLString
    cache_ok = True
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is not None:
            return UUID(value)
        return value

class Workspace(SQLModel, table=True):
    __tablename__ = "workspace"
    
    id: UUID = Field(
        default_factory=uuid4, 
        sa_column=Column(SQLiteUUID, primary_key=True, unique=True, nullable=False)
    )
    name: str = Field(nullable=False)
    
    integrations: list["WorkspaceIntegrationLink"] = Relationship(back_populates="workspace")


class Integration(SQLModel, table=True):
    __tablename__ = "integration"
    
    id: UUID = Field(
        default_factory=uuid4, 
        sa_column=Column(SQLiteUUID, primary_key=True, unique=True, nullable=False)
    )
    name: str = Field(nullable=False)
    
    workspaces: list["WorkspaceIntegrationLink"] = Relationship(back_populates="integration")


class WorkspaceIntegrationLink(SQLModel, table=True):
    __tablename__ = "workspace_integration_link"
    
    workspace_id: UUID = Field(
        sa_column=Column(SQLiteUUID, ForeignKey("workspace.id"), primary_key=True, nullable=False)
    )
    integration_id: UUID = Field(
        sa_column=Column(SQLiteUUID, ForeignKey("integration.id"), primary_key=True, nullable=False)
    )
    auth_details: dict = Field(
        default={}, 
        sa_column=Column(Text)
    )
    created_date: datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column=Column(DateTime, nullable=False)
    )
    
    workspace: Workspace = Relationship(back_populates="integrations")
    integration: Integration = Relationship(back_populates="workspaces")
