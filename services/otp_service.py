from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from models.otp_model import OTPModel
from utils.otp_utils import generate_otp, otp_expiry_time
from utils.send_mail_utils import send_otp_email
from utils.logger import get_logger

OTP_RESEND_COOLDOWN_SECONDS = 60  # 1 minute

logger = get_logger(__name__)

async def send_otp_service(email: str, db: Session):
    existing_otp = db.query(OTPModel).filter(OTPModel.email == email).first()
    now = datetime.now(timezone.utc)

    if existing_otp and not existing_otp.is_verified:
        time_diff = (now - existing_otp.created_at).total_seconds()
        if time_diff < OTP_RESEND_COOLDOWN_SECONDS:
            wait_time = int(OTP_RESEND_COOLDOWN_SECONDS - time_diff)
            raise HTTPException(
                status_code=429,
                detail=f"Please wait {wait_time} seconds before requesting a new OTP."
            )
        db.delete(existing_otp)
        db.commit()

    otp = generate_otp()
    otp_entry = OTPModel(
        email=email,
        otp=otp,
        is_verified=False,
        expires_at=otp_expiry_time()
    )
    db.add(otp_entry)
    db.commit()

    await send_otp_email(email, otp)
    logger.info(f"OTP sent to {email}")
    return {"message": f"OTP sent successfully to {email}"}


def verify_otp_service(email: str, otp: str, db: Session):
    otp_record = db.query(OTPModel).filter(OTPModel.email == email).first()
    now = datetime.now(timezone.utc)

    if not otp_record:
        raise HTTPException(status_code=404, detail="No OTP found for this email.")
    if otp_record.is_verified:
        raise HTTPException(status_code=400, detail="OTP already verified.")
    if now > otp_record.expires_at:
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired.")
    if otp_record.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP.")

    otp_record.is_verified = True
    db.commit()
    logger.info(f"OTP verified for {email}")
    return {"message": "OTP verified successfully!"}
