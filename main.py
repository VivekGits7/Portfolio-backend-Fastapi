from fastapi import FastAPI
from routes.contact_routes import router as contact_router
from routes.resume_routes import router as resume_router
from routes.otp_routes import router as otp_router
from database import engine
from models import contact_model
from models import otp_model
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Portfolio API")

# ✅ Include routers
app.include_router(contact_router)
app.include_router(resume_router)
app.include_router(otp_router)

# ✅ Create database tables
contact_model.Base.metadata.create_all(bind=engine)
otp_model.Base.metadata.create_all(bind=engine)

# ✅ Home endpoint for resume API
@app.get("/")
def home():
    return {"message": "Welcome to the Resume Management API"}
