from pydantic import BaseModel

class Email(BaseModel):
    subject: str
    body: str

class SentimentAnalysisResult(BaseModel):
    sentiment: str
    priority: str

class Reply(BaseModel):
    reply: str