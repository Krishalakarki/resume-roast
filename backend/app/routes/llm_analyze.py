from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.utils.deps import get_current_user
from app.services.llm import roast_resume

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.models import RoastHistory, Payment

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


    # 🔥 CHECK PREMIUM PAYMENT FIRST
    payment = db.query(Payment).filter(
        Payment.user_email == user,
        Payment.status == "SUCCESS"
    ).first()


    if not payment:

        return {
            "message": "Please complete payment first"
        }



    # 🔥 RATE LIMIT CHECK
    if not is_allowed(user):

        raise HTTPException(
            status_code=429,
            detail="Too many requests. Try again later."
        )



    text = ""



    # Extract PDF
    if file.filename.endswith(".pdf"):


        content = await file.read()

        reader = PdfReader(
            io.BytesIO(content)
        )


        for page in reader.pages:

            text += page.extract_text() or ""



    # Extract TXT
    elif file.filename.endswith(".txt"):


        text = (
            await file.read()
        ).decode("utf-8")



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




    # 🚀 CALL GROQ ONLY AFTER PAYMENT CHECK
    result = roast_resume(text)




    # Clean Groq response

    if hasattr(result, "choices"):

        roast_text = result.choices[0].message.content



    elif isinstance(result, dict):

        roast_text = (
            result.get("choices", [{}])[0]
            .get("message", {})
            .get("content", str(result))
        )


    else:

        roast_text = str(result)




    # Save history

    new_entry = RoastHistory(

        user_email=user,

        filename=file.filename,

        resume_text=text,

        ai_response=roast_text

    )



    db.add(new_entry)

    db.commit()

    db.refresh(new_entry)




    return {


        "message": "Premium roast completed",

        "user": user,

        "filename": file.filename,

        "result": roast_text

    }







# Get roast history

@router.get("/history")
def get_history(

    user: str = Depends(get_current_user),

    db: Session = Depends(get_db)

):


    history = db.query(RoastHistory).filter(

        RoastHistory.user_email == user

    ).all()



    return history