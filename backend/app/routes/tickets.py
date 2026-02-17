from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.project import Ticket
from app.schemas.project import Ticket as TicketSchema, TicketCreate, TicketUpdate
from app.models.user import User

router = APIRouter()

@router.get("", response_model=List[TicketSchema])
def read_tickets(
    db: Session = Depends(deps.get_db),
    project_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tickets.
    """
    query = db.query(Ticket)
    if project_id:
        query = query.filter(Ticket.project_id == project_id)
    
    tickets = query.offset(skip).limit(limit).all()
    return tickets

@router.post("", response_model=TicketSchema)
def create_ticket(
    *,
    db: Session = Depends(deps.get_db),
    ticket_in: TicketCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new ticket.
    """
    ticket = Ticket(**ticket_in.dict())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@router.get("/{id}", response_model=TicketSchema)
def read_ticket(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get ticket by ID.
    """
    ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.patch("/{id}", response_model=TicketSchema)
def update_ticket(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    ticket_in: TicketUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a ticket.
    """
    ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket_data = ticket_in.dict(exclude_unset=True)
    for field, value in ticket_data.items():
        setattr(ticket, field, value)
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@router.delete("/{id}", response_model=TicketSchema)
def delete_ticket(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a ticket.
    """
    ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db.delete(ticket)
    db.commit()
    return ticket
