from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.contact_create_model import ContactCreate
from database import session

from services.contact_service import (
    create_contact_service,
    get_contacts_service,
    get_contact_by_id_service,
    delete_contact_by_id_service,
    delete_contact_service
)

router = APIRouter(tags=["Contact"])

# ✅ Dependency for database session
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

# -------------------Creating a contact endpoints-------------------------------

# ✅ Route to submit contact form
@router.post("/contact")   #? https://locallhost:8000/contact
async def create_contact_controller(contact: ContactCreate, db: Session = Depends(get_db)):
    return await create_contact_service(contact, db)

# ✅ Route to get all contacts
@router.get("/contacts")   #? https://locallhost:8000/contacts
def get_contacts_controller(db: Session = Depends(get_db)):
    return get_contacts_service(db)

# ✅ Route to get a contact by ID
@router.get("/contacts/{contact_id}")   #? https://locallhost:8000/contacts/{contact_id}
def get_contact_controller(contact_id: str, db: Session = Depends(get_db)):
    return get_contact_by_id_service(contact_id, db)

# ✅ Route to delete all contacts
@router.delete("/contacts")   #? https://locallhost:8000/contacts
def delete_all_contacts_controller(db: Session = Depends(get_db)):
    return delete_contact_service(db)

# ✅ Route to delete a contact by ID
@router.delete("/contacts/{contact_id}")   #? https://locallhost:8000/contacts/{contact_id}
def delete_contact_controller(contact_id: str, db: Session = Depends(get_db)):
    return delete_contact_by_id_service(contact_id, db)
# -------------------End of contact endpoints-------------------------------