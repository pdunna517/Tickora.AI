from typing import Any
from pydantic import BaseModel

from fastapi import APIRouter, Depends
from app.api import deps
from app.models.user import User
from app.services.ai_service import ai_service

router = APIRouter()

class GenerateEpicsRequest(BaseModel):
    project_context: str

class TicketAssistRequest(BaseModel):
    ticket_content: str

@router.post("/generate-epics")
def generate_epics(
    request: GenerateEpicsRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return ai_service.generate_epics(request.project_context)

@router.post("/ticket-assist")
def ticket_assist(
    request: TicketAssistRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return ai_service.ticket_assist(request.ticket_content)
