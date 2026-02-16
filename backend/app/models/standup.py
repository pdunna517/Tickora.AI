from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Date, Integer, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum
from app.db.base import Base

class SessionStatus(str, enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"

class StandupConfig(Base):
    __tablename__ = "standup_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    time = Column(String) # HH:MM
    timezone = Column(String, default="UTC")
    working_days = Column(JSON) # e.g., ["Mon", "Tue", "Wed", "Thu", "Fri"]
    response_window_hours = Column(Integer, default=2)
    is_active = Column(Boolean, default=True)
    questions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project")
    sessions = relationship("StandupSession", back_populates="config")

class StandupSession(Base):
    __tablename__ = "standup_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    config_id = Column(UUID(as_uuid=True), ForeignKey("standup_configs.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    ends_at = Column(DateTime)
    status = Column(Enum(SessionStatus), default=SessionStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)

    config = relationship("StandupConfig", back_populates="sessions")
    responses = relationship("StandupResponse", back_populates="session")
    summary = relationship("StandupSummary", back_populates="session", uselist=False)

class StandupResponse(Base):
    __tablename__ = "standup_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("standup_sessions.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    yesterday = Column(Text)
    today = Column(Text)
    blockers = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    session = relationship("StandupSession", back_populates="responses")

class StandupSummary(Base):
    __tablename__ = "standup_summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("standup_sessions.id"))
    summary_text = Column(Text)
    blockers_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("StandupSession", back_populates="summary")

