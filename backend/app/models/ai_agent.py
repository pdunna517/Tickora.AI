from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, JSON, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime
from app.db.base import Base

class AIStatus(str, enum.Enum):
    DRAFT_AI_GENERATED = "draft_ai_generated"
    APPROVED = "approved"
    REJECTED = "rejected"

class PRDDocument(Base):
    __tablename__ = "prd_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    filename = Column(String)
    raw_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project")

class Epic(Base):
    __tablename__ = "ai_epics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    prd_id = Column(UUID(as_uuid=True), ForeignKey("prd_documents.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(AIStatus), default=AIStatus.DRAFT_AI_GENERATED)
    created_by_ai = Column(Boolean, default=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project")
    prd = relationship("PRDDocument")
    approver = relationship("User")
    stories = relationship("UserStory", back_populates="epic", cascade="all, delete-orphan")

class UserStory(Base):
    __tablename__ = "ai_user_stories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    epic_id = Column(UUID(as_uuid=True), ForeignKey("ai_epics.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    acceptance_criteria = Column(JSON) # List of strings
    priority = Column(String)
    status = Column(Enum(AIStatus), default=AIStatus.DRAFT_AI_GENERATED)
    created_by_ai = Column(Boolean, default=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    epic = relationship("Epic", back_populates="stories")

class RoadmapPhase(Base):
    __tablename__ = "ai_roadmap_phases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name = Column(String, nullable=False)
    epic_ids = Column(JSON) # Ordered list of epic IDs
    description = Column(Text)
    sequence = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class AIAnalysisLog(Base):
    __tablename__ = "ai_analysis_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    task_type = Column(String) # epics, stories, roadmap
    prompt_sent = Column(Text)
    response_received = Column(Text)
    is_valid_json = Column(Boolean)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
