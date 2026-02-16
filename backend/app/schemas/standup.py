from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, Field

# Configuration Schemas
class StandupConfigBase(BaseModel):
    project_id: UUID
    time: str = Field(..., pattern=r"^\d{2}:\d{2}$") # HH:MM
    timezone: str = "UTC"
    working_days: List[str] = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    response_window_hours: int = 2
    questions: List[str] = ["What did you do yesterday?", "What will you do today?", "Any blockers?"]

class StandupConfigCreate(StandupConfigBase):
    pass

class StandupConfigUpdate(BaseModel):
    time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    timezone: Optional[str] = None
    working_days: Optional[List[str]] = None
    response_window_hours: Optional[int] = None
    questions: Optional[List[str]] = None

class StandupConfig(StandupConfigBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Session Schemas
class StandupSessionBase(BaseModel):
    config_id: UUID
    date: date
    status: str = "active"

class StandupSession(StandupSessionBase):
    id: UUID
    created_at: datetime
    closes_at: Optional[datetime]

    class Config:
        from_attributes = True

# Response Schemas
class StandupResponseBase(BaseModel):
    session_id: UUID
    yesterday: str
    today: str
    blockers: Optional[str] = ""

class StandupResponseCreate(StandupResponseBase):
    pass

class StandupResponse(StandupResponseBase):
    id: UUID
    user_id: UUID
    config_id: UUID
    date: date
    created_at: datetime

    class Config:
        from_attributes = True

# Summary Schemas
class StandupSummary(BaseModel):
    blockers: List[Any] = []
    in_progress: List[Any] = []
    completed: List[Any] = []
    no_response: List[Any] = []

class StandupSessionSummary(BaseModel):
    id: UUID
    date: date
    summary: StandupSummary
    id_closed: bool
