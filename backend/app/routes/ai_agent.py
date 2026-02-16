from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.ai_agent import PRDDocument, Epic, UserStory, RoadmapPhase, AIAnalysisLog, AIStatus
from app.schemas import ai_agent as schemas
from app.services.ai_service import ai_service
import json

router = APIRouter()

@router.post("/upload-prd", response_model=schemas.PRDDocument)
async def upload_prd(
    project_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    content = await file.read()
    if file.filename.endswith(".pdf"):
        text = ai_service.extract_text_from_pdf(content)
    else:
        text = content.decode("utf-8")
    
    doc = PRDDocument(
        project_id=project_id,
        filename=file.filename,
        raw_text=text
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

@router.post("/generate-epics", response_model=List[schemas.Epic])
async def generate_epics(
    project_id: UUID,
    prd_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    prd = db.query(PRDDocument).filter(PRDDocument.id == prd_id).first()
    if not prd:
        raise HTTPException(status_code=404, detail="PRD not found")

    prompt = f"Extract Epics from this PRD:\n{prd.raw_text[:2000]}"
    ai_response = await ai_service.generate_structured_output(prompt, schemas.EpicGenerationResponse)
    
    # Log the analysis
    log = AIAnalysisLog(
        project_id=project_id,
        task_type="epics",
        prompt_sent=prompt,
        response_received=json.dumps(ai_response),
        is_valid_json=True
    )
    db.add(log)
    
    generated_epics = []
    for e_data in ai_response.get("epics", []):
        epic = Epic(
            project_id=project_id,
            prd_id=prd_id,
            title=e_data["title"],
            description=e_data["description"]
        )
        db.add(epic)
        generated_epics.append(epic)
    
    db.commit()
    return generated_epics

@router.post("/generate-stories", response_model=List[schemas.UserStory])
async def generate_stories(
    epic_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    epic = db.query(Epic).filter(Epic.id == epic_id).first()
    if not epic:
        raise HTTPException(status_code=404, detail="Epic not found")

    prompt = f"Generate User Stories for this Epic: {epic.title}\nDescription: {epic.description}"
    ai_response = await ai_service.generate_structured_output(prompt, schemas.StoryGenerationResponse)
    
    generated_stories = []
    for s_data in ai_response.get("stories", []):
        story = UserStory(
            epic_id=epic_id,
            title=s_data["title"],
            description=s_data["description"],
            acceptance_criteria=s_data["acceptance_criteria"],
            priority=s_data["priority"]
        )
        db.add(story)
        generated_stories.append(story)
    
    db.commit()
    return generated_stories

@router.post("/generate-roadmap", response_model=List[schemas.RoadmapPhase])
async def generate_roadmap(
    project_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    epics = db.query(Epic).filter(Epic.project_id == project_id).all()
    if not epics:
        raise HTTPException(status_code=400, detail="No epics found for roadmap generation")

    prompt = "Generate a sequenced Roadmap from these Epics."
    ai_response = await ai_service.generate_structured_output(prompt, schemas.RoadmapGenerationResponse)
    
    generated_phases = []
    for p_data in ai_response.get("phases", []):
        phase = RoadmapPhase(
            project_id=project_id,
            name=p_data["name"],
            description=p_data["description"],
            sequence=p_data["sequence"],
            epic_ids=[str(e_id) for e_id in p_data["epic_ids"]]
        )
        db.add(phase)
        generated_phases.append(phase)
    
    db.commit()
    return generated_phases
