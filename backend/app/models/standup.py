from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base

class StandupConfig(Base):
    __tablename__ = "standup_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    schedule = Column(String) # deprecated, replaced by 'time'
    time = Column(String) # e.g., "09:30"
    timezone = Column(String, default="UTC") # e.g., "Asia/Kolkata"
    working_days = Column(JSON) # e.g., ["Mon", "Tue", "Wed", "Thu", "Fri"]
    response_window_hours = Column(Integer, default=2)
    questions = Column(JSON) # List of questions
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project")
    sessions = relationship("StandupSession", back_populates="config")

class StandupSession(Base):
    __tablename__ = "standup_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    config_id = Column(UUID(as_uuid=True), ForeignKey("standup_configs.id"))
    date = Column(Date, default=datetime.utcnow().date)
    status = Column(String, default="active") # active, closed
    created_at = Column(DateTime, default=datetime.utcnow)
    closes_at = Column(DateTime)

    config = relationship("StandupConfig", back_populates="sessions")
    responses = relationship("StandupResponse", back_populates="session")

class StandupResponse(Base):
    __tablename__ = "standup_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    config_id = Column(UUID(as_uuid=True), ForeignKey("standup_configs.id"))
    session_id = Column(UUID(as_uuid=True), ForeignKey("standup_sessions.id"))
    content = Column(JSON) # Legacy field
    yesterday = Column(Text)
    today = Column(Text)
    blockers = Column(Text)
    date = Column(Date, default=datetime.utcnow().date)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    config = relationship("StandupConfig")
    session = relationship("StandupSession", back_populates="responses")

class StandupSummary(Base):
    __tablename__ = "standup_summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    config_id = Column(UUID(as_uuid=True), ForeignKey("standup_configs.id"))
    session_id = Column(UUID(as_uuid=True), ForeignKey("standup_sessions.id"))
    summary_content = Column(Text)
    date = Column(Date, default=datetime.utcnow().date)
    created_at = Column(DateTime, default=datetime.utcnow)

    config = relationship("StandupConfig")

