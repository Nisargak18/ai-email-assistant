from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.email_router import router as email_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_router, prefix="/api", tags=["emails"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Email Assistant API"}