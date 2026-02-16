from typing import Any
from fastapi import APIRouter, UploadFile, File, Depends
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.post("/prd")
def upload_prd(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return {"filename": file.filename, "status": "processed", "type": "prd"}

@router.post("/architecture")
def upload_architecture(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return {"filename": file.filename, "status": "processed", "type": "architecture"}
