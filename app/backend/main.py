from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from app.backend.routers.email_router import router as email_router

app = FastAPI(title="AI Email Assistant API", version="1.0.0")

# Allowed frontend origins (Vite on 5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

#  CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Explicitly allow frontend
    allow_credentials=True,
    allow_methods=["*"],         # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],         # Allow all headers
)

@app.get("/", include_in_schema=False)
def root():
    return {"message": "AI Email Assistant API is running."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Avoid 404 for browser favicon requests
@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    return Response(status_code=204)

# Include email router
app.include_router(email_router)
