from typing import Any, List, Optional
from uuid import UUID
from datetime import date, datetime
import pytz

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.standup import StandupConfig, StandupResponse, StandupSummary, StandupSession
from app.models.user import User
from app.schemas import standup as schemas

router = APIRouter()

@router.post("/configure", response_model=schemas.StandupConfig)
def configure_standup(
    *,
    db: Session = Depends(deps.get_db),
    config_in: schemas.StandupConfigCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Configure automated standups for a project.
    """
    # Verify timezone
    try:
        pytz.timezone(config_in.timezone)
    except pytz.UnknownTimeZoneError:
        raise HTTPException(status_code=400, detail="Invalid timezone")

    config = StandupConfig(**config_in.dict())
    db.add(config)
    db.commit()
    db.refresh(config)
    return config

@router.post("/respond", response_model=schemas.StandupResponse)
def respond_to_standup(
    *,
    db: Session = Depends(deps.get_db),
    response_in: schemas.StandupResponseCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Submit a standup response for an active session.
    """
    session = db.query(StandupSession).filter(
        StandupSession.id == response_in.session_id,
        StandupSession.status == "active"
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Active standup session not found")

    # Check for existing response
    existing = db.query(StandupResponse).filter(
        StandupResponse.session_id == session.id,
        StandupResponse.user_id == current_user.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Response already submitted for this session")

    response = StandupResponse(
        **response_in.dict(),
        user_id=current_user.id,
        config_id=session.config_id,
        date=session.date
    )
    db.add(response)
    db.commit()
    db.refresh(response)
    return response

@router.get("/summary/{session_id}", response_model=schemas.StandupSummary)
def get_standup_summary(
    session_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get categorized summary of a standup session.
    """
    session = db.query(StandupSession).filter(StandupSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    responses = db.query(StandupResponse).filter(StandupResponse.session_id == session_id).all()
    
    # Categorization logic
    summary = {
        "blockers": [],
        "in_progress": [],
        "completed": [],
        "no_response": []
    }
    
    responded_user_ids = set()
    for r in responses:
        responded_user_ids.add(r.user_id)
        user_info = {"user_id": r.user_id, "name": "User"} # In real app, join with User model
        
        if r.blockers and r.blockers.strip():
            summary["blockers"].append({**user_info, "content": r.blockers})
        
        if r.today and r.today.strip():
            summary["in_progress"].append({**user_info, "content": r.today})
            
        if r.yesterday and r.yesterday.strip():
            summary["completed"].append({**user_info, "content": r.yesterday})

    # Placeholder: Identify users who haven't responded
    # In a real app, you'd get all members of the project and diff with responded_user_ids
    
    return summary

@router.get("/active-sessions", response_model=List[schemas.StandupSession])
def list_active_sessions(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List currently active standup sessions.
    """
    sessions = db.query(StandupSession).filter(StandupSession.status == "active").all()
    return sessions

