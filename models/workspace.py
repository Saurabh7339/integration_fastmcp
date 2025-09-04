from datetime import datetime
from typing import List, TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB

if TYPE_CHECKING:
    from .workspace import WorkspaceIntegrationLink

class Workspace(SQLModel, table=True):
    __tablename__ = "workspace"
    
    id: UUID = Field(
        default_factory=uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    )
    name: str = Field(nullable=False)
    description: str = Field(nullable=False, default="Default workspace description")
    default_llm_provider: UUID = Field(nullable=False)
    default_embedding_provider: UUID = Field(nullable=False)
    default_embedding_model: UUID = Field(nullable=False)
    default_llm_model: UUID = Field(nullable=False)
    is_active: bool = Field(nullable=False, default=True)
    is_public: bool = Field(nullable=False, default=False)
    organization_id: UUID = Field(nullable=False)
    created_by_id: UUID = Field(nullable=False)
    created_date: datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column=Column(DateTime, nullable=False)
    )
    last_updated_date: datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column=Column(DateTime, nullable=False)
    )
    
    integrations: List["WorkspaceIntegrationLink"] = Relationship(back_populates="workspace")


class Integration(SQLModel, table=True):
    __tablename__ = "integration"
    
    id: UUID = Field(
        default_factory=uuid4, 
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    )
    name: str = Field(nullable=False)
    
    workspaces: List["WorkspaceIntegrationLink"] = Relationship(back_populates="integration")


class WorkspaceIntegrationLink(SQLModel, table=True):
    __tablename__ = "workspace_integration_link"
    
    workspace_id: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("workspace.id"), primary_key=True, nullable=False)
    )
    integration_id: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("integration.id"), primary_key=True, nullable=False)
    )
    auth_details: dict = Field(
        default_factory=dict, 
        sa_column=Column(JSONB, nullable=False, default={})
    )
    created_date: datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column=Column(DateTime, nullable=False)
    )
    
    workspace: "Workspace" = Relationship(back_populates="integrations")
    integration: "Integration" = Relationship(back_populates="workspaces")
