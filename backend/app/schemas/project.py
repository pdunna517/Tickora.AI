from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime, date
from app.models.project import TicketStatus, TicketPriority, SprintStatus

# Shared properties
class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    name: str

class ProjectUpdate(ProjectBase):
    pass

class ProjectInDBBase(ProjectBase):
    id: UUID4
    owner_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Project(ProjectInDBBase):
    pass

# Sprint Schemas
class SprintBase(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[SprintStatus] = SprintStatus.PLANNED
    project_id: Optional[UUID4] = None

class SprintCreate(SprintBase):
    name: str
    project_id: UUID4

class SprintUpdate(SprintBase):
    pass

class Sprint(SprintBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Ticket Schemas
class TicketBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = TicketStatus.TODO
    priority: Optional[TicketPriority] = TicketPriority.MEDIUM
    points: Optional[int] = None
    assignee_id: Optional[UUID4] = None
    sprint_id: Optional[UUID4] = None

class TicketCreate(TicketBase):
    title: str

class TicketUpdate(TicketBase):
    pass

class Ticket(TicketBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
