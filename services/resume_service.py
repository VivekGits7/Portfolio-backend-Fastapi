import os
import shutil
from fastapi import HTTPException
from fastapi.responses import FileResponse

# Folder to store the resume file
UPLOAD_FOLDER = "uploads"
RESUME_PATH = os.path.join(UPLOAD_FOLDER, "VIVEK VISHWAKARMA RESUME.pdf")

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_resume_service():
    if not os.path.exists(RESUME_PATH):
        raise HTTPException(status_code=404, detail="Resume not found")
    return FileResponse(
        RESUME_PATH,
        media_type="application/pdf",
        filename="VIVEK VISHWAKARMA RESUME.pdf"
    )

def update_resume_service(file):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    with open(RESUME_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"Resume '{file.filename}' uploaded successfully."}

