from typing import Any, List, Optional
from uuid import UUID
from datetime import datetime
import pytz

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.models.standup import StandupConfig, StandupResponse, StandupSummary, StandupSession, SessionStatus
from app.models.user import User
from app.schemas import standup as schemas
from app.services.standup_service import standup_service

router = APIRouter()

@router.post("/configure", response_model=schemas.StandupConfig)
def configure_standup(
    *,
    db: Session = Depends(deps.get_db),
    config_in: schemas.StandupConfigCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create or update standup config for a project.
    """
    # Verify timezone
    try:
        pytz.timezone(config_in.timezone)
    except pytz.UnknownTimeZoneError:
        raise HTTPException(status_code=400, detail="Invalid timezone")

    config = db.query(StandupConfig).filter(StandupConfig.project_id == config_in.project_id).first()
    if config:
        # Update existing
        for field, value in config_in.dict(exclude_unset=True).items():
            setattr(config, field, value)
    else:
        # Create new
        config = StandupConfig(**config_in.dict())
        db.add(config)
    
    db.commit()
    db.refresh(config)
    return config

@router.get("/active", response_model=Optional[schemas.StandupSession])
def get_active_session(
    *,
    db: Session = Depends(deps.get_db),
    project_id: UUID = Query(...),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return active session for project.
    """
    session = db.query(StandupSession).filter(
        StandupSession.project_id == project_id,
        StandupSession.status == SessionStatus.ACTIVE
    ).first()
    return session

@router.post("/respond", response_model=schemas.StandupResponse)
def respond_to_standup(
    *,
    db: Session = Depends(deps.get_db),
    response_in: schemas.StandupResponseCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Authenticated users submit standup response.
    Ensure only one response per user per session (Upsert logic).
    """
    session = db.query(StandupSession).filter(
        StandupSession.id == response_in.session_id,
        StandupSession.status == SessionStatus.ACTIVE
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Active standup session not found")

    # Check for existing response (Upsert)
    response = db.query(StandupResponse).filter(
        StandupResponse.session_id == session.id,
        StandupResponse.user_id == current_user.id
    ).first()
    
    if response:
        # Update
        response.yesterday = response_in.yesterday
        response.today = response_in.today
        response.blockers = response_in.blockers
    else:
        # Create
        response = StandupResponse(
            **response_in.dict(),
            user_id=current_user.id
        )
        db.add(response)
    
    db.commit()
    db.refresh(response)
    
    # Process for ticket updates (Async-like but synchronous for simplicity here)
    standup_service.process_response(db, response.id)
    
    return response

@router.get("/summary/{session_id}", response_model=schemas.StandupSummary)
def get_standup_summary(
    session_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Return generated summary.
    """
    summary = db.query(StandupSummary).filter(StandupSummary.session_id == session_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found. It might still be generating or the session is active.")
    return summary

