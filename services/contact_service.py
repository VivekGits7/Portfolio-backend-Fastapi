from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from database import session


from utils.send_mail_utils import send_email
from models.contact_model import Contact
from models.contact_create_model import ContactCreate
from models.otp_model import OTPModel



async def create_contact_service(contact: ContactCreate, db: session):
    otp_record = db.query(OTPModel).filter(OTPModel.email == contact.email).first()

    if not otp_record or not otp_record.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified. Please verify OTP first.")

    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)

    try:
        db.commit()
        db.refresh(db_contact)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Contact with email '{contact.email}' already exists."
        )

    # Send email notification
    await send_email(contact)

    return {"id": db_contact.id, "message": "Your message has been sent successfully!"}

def get_contacts_service(db: session):
    return db.query(Contact).all()

def get_contact_by_id_service(contact_id: str, db: session):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

def delete_contact_service(db: session):
    deleted = db.query(Contact).delete()
    db.commit()
    return {"message": f"Deleted {deleted} contacts successfully"}

def delete_contact_by_id_service(contact_id: str, db: session):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted successfully"}