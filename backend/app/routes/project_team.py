from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.project import Project, ProjectMember, ProjectMemberRole
from app.schemas import project_member as schemas
from app.core.security import get_password_hash
import uuid

router = APIRouter()

def get_project_admin(
    project_id: UUID, 
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_active_user)
) -> User:
    # Check if user is project owner or an admin member
    project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id == current_user.id:
        return current_user
        
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    
    if not member or member.role != ProjectMemberRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project admins can manage the team"
        )
    return current_user

@router.post("/invite", response_model=schemas.ProjectMember)
def invite_member(
    project_id: UUID,
    invite: schemas.ProjectMemberInvite,
    db: Session = Depends(deps.get_db),
    admin: User = Depends(get_project_admin)
) -> Any:
    # Check if user already exists
    user = db.query(User).filter(User.email == invite.email).first()
    if not user:
        # Create inactive user
        user = User(
            email=invite.email,
            hashed_password=get_password_hash(str(uuid.uuid4())), # Placeholder password
            full_name=invite.email.split("@")[0],
            is_active=False
        )
        db.add(user)
        db.flush() # Get user ID
    
    # Check if already a member
    existing_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member of this project")
    
    member = ProjectMember(
        project_id=project_id,
        user_id=user.id,
        role=invite.role
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    
    # Return member with email
    res = schemas.ProjectMember.from_orm(member)
    res.email = user.email
    return res

@router.get("/", response_model=List[schemas.ProjectMember])
def list_members(
    project_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    # Verify user is a member of the project
    member_check = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    
    project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    if not member_check and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not a member of this project")

    members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
    
    res = []
    for m in members:
        sm = schemas.ProjectMember.from_orm(m)
        sm.email = m.user.email
        res.append(sm)
    return res

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    project_id: UUID,
    user_id: UUID,
    db: Session = Depends(deps.get_db),
    admin: User = Depends(get_project_admin)
) -> Any:
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
        
    # Prevent removing the project owner
    project = db.query(Project).get(project_id)
    if user_id == project.owner_id:
        raise HTTPException(status_code=400, detail="Cannot remove project owner")
        
    db.delete(member)
    db.commit()
    return None
