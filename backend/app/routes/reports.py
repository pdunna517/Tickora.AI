from typing import Any
from fastapi import APIRouter, Depends
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.get("/velocity")
def get_velocity(current_user: User = Depends(deps.get_current_active_user)) -> Any:
    return {"velocity": 45, "trend": "stable"}

@router.get("/blockers")
def get_blockers(current_user: User = Depends(deps.get_current_active_user)) -> Any:
    return {"blockers": ["API Rate limits", "Design pending"]}

@router.get("/sprint/{id}")
def get_sprint_report(id: str, current_user: User = Depends(deps.get_current_active_user)) -> Any:
    return {"sprint_id": id, "completed_points": 20, "carry_over": 5}
