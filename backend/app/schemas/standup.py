from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
import enum

class SessionStatus(str, enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"

# Configuration Schemas
class StandupConfigBase(BaseModel):
    project_id: UUID
    time: str = Field(..., pattern=r"^([01]\d|2[0-3]):([0-5]\d)$", description="Format HH:MM")
    timezone: Optional[str] = "UTC"
    working_days: List[str] = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    response_window_hours: int = 2
    is_active: bool = True
    questions: List[str] = ["What did you do yesterday?", "What will you do today?", "Any blockers?"]

class StandupConfigCreate(StandupConfigBase):
    pass

class StandupConfigUpdate(BaseModel):
    time: Optional[str] = Field(None, pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")
    timezone: Optional[str] = None
    working_days: Optional[List[str]] = None
    response_window_hours: Optional[int] = None
    is_active: Optional[bool] = None
    questions: Optional[List[str]] = None

class StandupConfig(StandupConfigBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Session Schemas
class StandupSessionBase(BaseModel):
    project_id: UUID
    config_id: UUID
    started_at: datetime
    ends_at: datetime
    status: SessionStatus = SessionStatus.ACTIVE

class StandupSession(StandupSessionBase):
    id: UUID
    created_at: datetime

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
    created_at: datetime

    class Config:
        from_attributes = True

# Summary Schemas
class StandupSummaryBase(BaseModel):
    session_id: UUID
    summary_text: str
    blockers_json: Optional[Any] = None

class StandupSummary(StandupSummaryBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
