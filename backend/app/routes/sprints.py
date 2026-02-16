from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.project import Sprint, Project
from app.schemas.project import Sprint as SprintSchema, SprintCreate, SprintUpdate
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[SprintSchema])
def read_sprints(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve sprints.
    """
    # Simply returning all sprints for now, likely need filtering by project
    sprints = db.query(Sprint).offset(skip).limit(limit).all()
    return sprints

@router.post("", response_model=SprintSchema)
def create_sprint(
    *,
    db: Session = Depends(deps.get_db),
    sprint_in: SprintCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new sprint.
    """
    # Verify project exists and user has access
    project = db.query(Project).filter(Project.id == sprint_in.project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    sprint = Sprint(**sprint_in.dict())
    db.add(sprint)
    db.commit()
    db.refresh(sprint)
    return sprint

@router.get("/{id}", response_model=SprintSchema)
def read_sprint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get sprint by ID.
    """
    sprint = db.query(Sprint).filter(Sprint.id == id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint

@router.put("/{id}", response_model=SprintSchema)
def update_sprint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    sprint_in: SprintUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a sprint.
    """
    sprint = db.query(Sprint).filter(Sprint.id == id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    sprint_data = sprint_in.dict(exclude_unset=True)
    for field, value in sprint_data.items():
        setattr(sprint, field, value)
    
    db.add(sprint)
    db.commit()
    db.refresh(sprint)
    return sprint

@router.delete("/{id}", response_model=SprintSchema)
def delete_sprint(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a sprint.
    """
    sprint = db.query(Sprint).filter(Sprint.id == id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    db.delete(sprint)
    db.commit()
    return sprint
