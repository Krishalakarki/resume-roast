from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.utils.deps import get_current_user
from app.services.llm import roast_resume

from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.database.models import RoastHistory
from app.utils.rate_limit import is_allowed
from pypdf import PdfReader
import io

router = APIRouter()


# Analyze resume + save history
@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # 🔥 RATE LIMIT CHECK (ADD THIS HERE)
    if not is_allowed(user):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Try again later."
        )

    text = ""

    # Extract PDF text
    if file.filename.endswith(".pdf"):

        content = await file.read()
        reader = PdfReader(io.BytesIO(content))

        for page in reader.pages:
            text += page.extract_text() or ""

    # Extract TXT text
    elif file.filename.endswith(".txt"):

        text = (await file.read()).decode("utf-8")

    else:
        raise HTTPException(
            status_code=400,
            detail="Only PDF or TXT allowed"
        )

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text"
        )

    # Send resume to LLM
    result = roast_resume(text)

    # Save AI result in database
    new_entry = RoastHistory(
        user_email=user,
        filename=file.filename,
        resume_text=text,
        ai_response=str(result)
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {
        "message": "Resume analyzed + saved",
        "user": user,
        "filename": file.filename,
        "result": result
    }


# Get user's roast history
@router.get("/history")
def get_history(
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    history = db.query(RoastHistory).filter(
        RoastHistory.user_email == user
    ).all()

    return history