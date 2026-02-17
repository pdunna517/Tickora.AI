from typing import Any, Dict
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from app.models.user import User
from app.models.project import Ticket, Project, Sprint, TicketStatus
from app.models.standup import StandupSession, StandupResponse

router = APIRouter()

@router.get("/metrics")
def get_dashboard_metrics(
    project_id: UUID = Query(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Returns real-time metrics for a specific project dashboard.
    """
    # Ticket counts by status
    ticket_metrics = db.query(
        Ticket.status, func.count(Ticket.id)
    ).filter(Ticket.project_id == project_id).group_by(Ticket.status).all()
    
    stats = {status.value: count for status, count in ticket_metrics}
    for s in TicketStatus:
        if s.value not in stats:
            stats[s.value] = 0

    # Active sprint info
    active_sprint = db.query(Sprint).filter(
        Sprint.project_id == project_id,
        Sprint.status == "active"
    ).first()

    # Standup completion (last 5 sessions)
    recent_sessions = db.query(StandupSession).filter(
        StandupSession.project_id == project_id
    ).order_by(StandupSession.created_at.desc()).limit(5).all()
    
    completion_rates = []
    for session in recent_sessions:
        responses = db.query(StandupResponse).filter(StandupResponse.session_id == session.id).count()
        # In a real app, we'd compare against actual member count
        completion_rates.append({
            "date": session.created_at.date().isoformat(),
            "responses": responses
        })

    return {
        "tickets": stats,
        "active_sprint": {
            "name": active_sprint.name if active_sprint else "No Active Sprint",
            "id": active_sprint.id if active_sprint else None
        },
        "standup_history": completion_rates
    }
