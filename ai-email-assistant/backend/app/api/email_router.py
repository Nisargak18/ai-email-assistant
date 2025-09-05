from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.email_processing import load_emails, analyze_email, generate_reply

router = APIRouter()

class EmailAnalysisRequest(BaseModel):
    body: str

class EmailResponseRequest(BaseModel):
    subject: str
    body: str

@router.get("/emails")
async def get_emails():
    try:
        emails = load_emails("path/to/mock_emails.csv")
        return {"emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_email(request: EmailAnalysisRequest):
    try:
        sentiment, priority = analyze_email(request.body)
        return {"sentiment": sentiment, "priority": priority}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/respond")
async def respond_to_email(request: EmailResponseRequest):
    try:
        reply = generate_reply(request.subject, request.body)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))