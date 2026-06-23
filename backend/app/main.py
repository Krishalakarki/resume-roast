from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.database.db import engine, Base
from app.database import models
from app.database.models import User, RoastHistory

from app.routes import auth, roast, llm_analyze

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# ---------------- CORS SETUP ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all frontend requests (React/HTML/etc)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTES ----------------
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(roast.router, prefix="/roast", tags=["Roast"])
app.include_router(llm_analyze.router, prefix="/llm_analyze", tags=["LLM"])

# ---------------- DB INIT ----------------
Base.metadata.create_all(bind=engine)

# ---------------- HOME ROUTE ----------------
@app.get("/")
def home():
    return {"message": "Resume Roaster API is running 🔥"}