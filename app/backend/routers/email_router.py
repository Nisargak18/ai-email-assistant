from typing import List
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

from app.backend.services.email_service import load_emails, generate_reply

# Router (works across FastAPI versions)
router = APIRouter(prefix="/emails", tags=["emails"])


# --- Models ---
class EmailItem(BaseModel):
    sender: str
    subject: str
    body: str
    date: str


class ReplyRequest(BaseModel):
    subject: str
    body: str


class ReplyResponse(BaseModel):
    reply: str


# --- Endpoints ---
@router.get("/", response_model=List[EmailItem])
def get_emails() -> List[EmailItem]:
    """
    Get all emails from CSV.
    """
    try:
        emails = load_emails()
        return [EmailItem(**e) for e in emails]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/generate-reply", response_model=ReplyResponse)
def post_generate_reply(request: ReplyRequest = Body(...)) -> ReplyResponse:
    """
    Generate AI-based reply for a given subject and body.
    """
    try:
        reply = generate_reply(request.subject, request.body)
        return ReplyResponse(reply=reply)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
