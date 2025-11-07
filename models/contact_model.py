from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, UUID, Column, DateTime, func
import uuid

Base = declarative_base()

class Contact(Base):

    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String)
    email = Column(String , unique=True)
    phone = Column(String , unique=True)
    subject = Column(String)
    message = Column(String)

    # ✅ Auto timestamp columns
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
