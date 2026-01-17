from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MoneyTrack API",
    description="Personal Finance Tracker API",
    version="1.0.0"
)

# CORS middleware - frontend ilə əlaqə üçün
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production-da dəyişəcəyik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """API-nin əsas endpoint-i"""
    return {
        "message": "MoneyTrack API-yə xoş gəldiniz!",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """API sağlamdır yoxsa yox - yoxlama"""
    return {"status": "healthy"}