from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from utils.logger import get_logger

from services.resume_service import (
    get_resume_service,
    update_resume_service
)

log = get_logger(__name__)

router = APIRouter(tags=["Resume"])

# ✅ 1. Get the resume PDF file
@router.get("/resume", response_class=FileResponse)
def get_resume_controller():
    log.info(f"Resuming resume")
    return get_resume_service()

# ✅ 2. Upload or update the resume
@router.post("/resume/upload")
def upload_resume_controller(file: UploadFile = File(...)):
    log.info(f"Uploading resume")
    return update_resume_service(file)


