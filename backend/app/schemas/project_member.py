from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.project import ProjectMemberRole

class ProjectMemberBase(BaseModel):
    user_id: UUID
    role: ProjectMemberRole

class ProjectMemberInvite(BaseModel):
    email: EmailStr
    role: ProjectMemberRole = ProjectMemberRole.MEMBER

class ProjectMember(BaseModel):
    id: UUID
    project_id: UUID
    user_id: UUID
    role: ProjectMemberRole
    joined_at: datetime
    email: Optional[str] = None # Added for list view

    class Config:
        from_attributes = True
