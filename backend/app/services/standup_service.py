import re
import logging
from uuid import UUID
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.standup import StandupConfig, StandupSession, StandupResponse, StandupSummary, SessionStatus
from app.models.project import Ticket, TicketStatus, Project
from app.services.ai_service import ai_service
from app.database import SessionLocal

logger = logging.getLogger(__name__)

class StandupService:
    def create_session(self, db: Session, config_id: UUID) -> StandupSession:
        config = db.query(StandupConfig).get(config_id)
        if not config:
            raise ValueError("Standup config not found")
        
        # Check if session already exists for this config on the same day
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        existing = db.query(StandupSession).filter(
            StandupSession.config_id == config_id,
            StandupSession.started_at >= today_start
        ).first()
        
        if existing:
            logger.info(f"Session already exists for config {config_id} today")
            return existing
            
        ends_at = now + timedelta(hours=config.response_window_hours)
        session = StandupSession(
            project_id=config.project_id,
            config_id=config.id,
            started_at=now,
            ends_at=ends_at,
            status=SessionStatus.ACTIVE
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        logger.info(f"Standup session created for project {config.project_id} at time {config.time} (timezone {config.timezone or 'UTC'})")
        return session

    def close_session(self, db: Session, session_id: UUID):
        session = db.query(StandupSession).get(session_id)
        if not session or session.status == SessionStatus.CLOSED:
            return
            
        session.status = SessionStatus.CLOSED
        db.commit()
        
        # Generate summary
        self.generate_standup_summary(db, session_id)
        logger.info(f"Closed standup session {session_id}")

    def process_response(self, db: Session, response_id: UUID):
        response = db.query(StandupResponse).get(response_id)
        if not response:
            return
            
        # Extract ticket IDs (e.g., TICK-123)
        text = f"{response.yesterday} {response.today} {response.blockers}"
        ticket_ids = re.findall(r'[A-Z]+-\d+', text)
        
        for t_id in set(ticket_ids):
            ticket = db.query(Ticket).filter(Ticket.title.contains(t_id)).first()
            if ticket:
                # Add comment logic (assuming a TicketComment model or similar, 
                # but for now we'll just simulate or use description if allowed)
                # For now, let's just log it as the request mentioned "Add comment"
                logger.info(f"Found ticket {t_id} in standup response {response_id}. Updating via automation.")
                
                # Simple status update logic
                lower_text = text.lower()
                if "completed" in lower_text or "done" in lower_text:
                    if t_id in response.yesterday.upper():
                        ticket.status = TicketStatus.DONE
                elif "in progress" in lower_text or "started" in lower_text:
                    if t_id in response.today.upper():
                        ticket.status = TicketStatus.IN_PROGRESS
        
        db.commit()

    def generate_standup_summary(self, db: Session, session_id: UUID) -> StandupSummary:
        session = db.query(StandupSession).get(session_id)
        responses = db.query(StandupResponse).filter(StandupResponse.session_id == session_id).all()
        
        if not responses:
            summary_text = "No responses received for this standup session."
            summary = StandupSummary(session_id=session_id, summary_text=summary_text, blockers_json=[])
            db.add(summary)
            db.commit()
            return summary

        # Prepare AI prompt
        prompt = "Summarize the following standup responses.\nFormat:\n1. 🔴 Blockers (highlight urgent)\n2. 🟡 In Progress\n3. 🟢 Completed Yesterday\n4. ⚠ No Response\nKeep summary concise and professional.\n\nResponses:\n"
        
        responders = []
        for r in responses:
            user = r.user
            responders.append(user.id)
            prompt += f"- User: {user.full_name or user.email}\n"
            prompt += f"  Yesterday: {r.yesterday}\n"
            prompt += f"  Today: {r.today}\n"
            prompt += f"  Blockers: {r.blockers}\n\n"

        # Identify non-responders (This would need project member lookup)
        # For now, we'll just note who responded
        
        ai_result = ai_service.generate_summary(prompt)
        
        summary = StandupSummary(
            session_id=session_id,
            summary_text=ai_result["summary_text"],
            blockers_json=ai_result["blockers_json"]
        )
        db.add(summary)
        db.commit()
        db.refresh(summary)
        return summary

standup_service = StandupService()
