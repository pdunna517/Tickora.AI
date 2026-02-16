from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.models.ai_agent import AIStatus

class PRDDocumentBase(BaseModel):
    project_id: UUID
    filename: str

class PRDDocument(PRDDocumentBase):
    id: UUID
    created_at: datetime
    class Config: from_attributes = True

class UserStoryBase(BaseModel):
    title: str
    description: str
    acceptance_criteria: List[str]
    priority: str

class UserStory(UserStoryBase):
    id: UUID
    epic_id: UUID
    status: AIStatus
    created_by_ai: bool
    class Config: from_attributes = True

class EpicBase(BaseModel):
    title: str
    description: str

class Epic(EpicBase):
    id: UUID
    project_id: UUID
    status: AIStatus
    created_by_ai: bool
    stories: List[UserStory] = []
    class Config: from_attributes = True

class RoadmapPhaseBase(BaseModel):
    name: str
    epic_ids: List[UUID]
    description: Optional[str] = None
    sequence: int

class RoadmapPhase(RoadmapPhaseBase):
    id: UUID
    class Config: from_attributes = True

class AIAnalysisLogBase(BaseModel):
    project_id: UUID
    task_type: str
    prompt_sent: str
    response_received: str
    is_valid_json: bool
    retry_count: int

class EpicGenerationResponse(BaseModel):
    epics: List[EpicBase]

class StoryGenerationResponse(BaseModel):
    stories: List[UserStoryBase]

class RoadmapGenerationResponse(BaseModel):
    phases: List[RoadmapPhaseBase]
