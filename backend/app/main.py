from app.core.database import connect_to_mongodb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.incidents.routes import router as incident_router

app = FastAPI(
    title="Incident Response Agent",
    description="AI-powered incident detection and response platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(incident_router)
@app.get("/")
async def root():
    return {
        "message": "Incident Response Agent API is running!",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "incident-response-agent"
    }
@app.get("/db-health")
async def database_health():
    try:
        database = connect_to_mongodb()

        return {
            "status": "connected",
            "database": database.name,
            "collections": database.list_collection_names()
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }