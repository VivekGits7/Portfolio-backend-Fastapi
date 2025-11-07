from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import session
from services.otp_service import send_otp_service, verify_otp_service
from utils.logger import get_logger

router = APIRouter(tags=["OTP Verification"])
log = get_logger(__name__)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.post("/send-otp")
async def send_otp(email: str, db: Session = Depends(get_db)):
    log.info(f"Sending OTP to {email}")
    return await send_otp_service(email, db)

@router.post("/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    log.info(f"Verifying OTP for {email}")
    return verify_otp_service(email, otp, db)
