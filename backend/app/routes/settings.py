from typing import Any, Optional
from pydantic import BaseModel, UUID4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.settings import Settings
from app.models.user import User

router = APIRouter()

# Schemas
class SettingsBase(BaseModel):
    theme: Optional[str] = "light"
    notifications: Optional[dict] = {}
    teams_webhook_url: Optional[str] = None

class SettingsUpdate(SettingsBase):
    pass

class SettingsSchema(SettingsBase):
    id: UUID4
    user_id: UUID4
    class Config:
        from_attributes = True

class WebhookUpdate(BaseModel):
    url: str

@router.get("", response_model=SettingsSchema)
def read_settings(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    settings = db.query(Settings).filter(Settings.user_id == current_user.id).first()
    if not settings:
        # Create default settings if not exists
        settings = Settings(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.put("", response_model=SettingsSchema)
def update_settings(
    *,
    db: Session = Depends(deps.get_db),
    settings_in: SettingsUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    settings = db.query(Settings).filter(Settings.user_id == current_user.id).first()
    if not settings:
        settings = Settings(user_id=current_user.id)
    
    settings_data = settings_in.dict(exclude_unset=True)
    for field, value in settings_data.items():
        setattr(settings, field, value)
    
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings

@router.post("/teams-webhook")
def update_teams_webhook(
    *,
    db: Session = Depends(deps.get_db),
    webhook_in: WebhookUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    settings = db.query(Settings).filter(Settings.user_id == current_user.id).first()
    if not settings:
        settings = Settings(user_id=current_user.id)
    
    settings.teams_webhook_url = webhook_in.url
    db.add(settings)
    db.commit()
    return {"status": "updated"}
