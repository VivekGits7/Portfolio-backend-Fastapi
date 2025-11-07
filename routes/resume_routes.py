from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse


from services.resume_service import (
    get_resume_service,
    update_resume_service
)

router = APIRouter(tags=["Resume"])

# ✅ 1. Get the resume PDF file
@router.get("/resume", response_class=FileResponse)
def get_resume_controller():
    return get_resume_service()

# ✅ 2. Upload or update the resume
@router.post("/resume/upload")
def upload_resume_controller(file: UploadFile = File(...)):
    return update_resume_service(file)


