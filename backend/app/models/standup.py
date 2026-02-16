from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.base import Base

class StandupConfig(Base):
    __tablename__ = "standup_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    schedule = Column(String) # e.g., "09:00"
    questions = Column(JSON) # List of questions
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project")

class StandupResponse(Base):
    __tablename__ = "standup_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    config_id = Column(UUID(as_uuid=True), ForeignKey("standup_configs.id"))
    content = Column(JSON) # Answers to questions
    date = Column(Date, default=datetime.utcnow().date)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    config = relationship("StandupConfig")

class StandupSummary(Base):
    __tablename__ = "standup_summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    config_id = Column(UUID(as_uuid=True), ForeignKey("standup_configs.id"))
    summary_content = Column(Text)
    date = Column(Date, default=datetime.utcnow().date)
    created_at = Column(DateTime, default=datetime.utcnow)

    config = relationship("StandupConfig")
