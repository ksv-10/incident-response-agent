
from datetime import datetime, timezone
from typing import Literal

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.incident_analyzer import analyze_incident

from app.core.database import connect_to_mongodb
from app.memory.memory_manager import recall_similar_incidents
from app.memory.memory_manager import (
    recall_similar_incidents,
    store_resolved_incident
)

router = APIRouter(prefix="/incidents", tags=["Incidents"])


# Request model for creating incidents
class IncidentCreate(BaseModel):
    title: str
    service: str
    severity: Literal["SEV-1", "SEV-2", "SEV-3", "SEV-4"]
    description: str


# Request model for searching incident memory
class MemorySearchRequest(BaseModel):
    query: str
    limit: int = 5


# Request model for resolving incidents
class IncidentResolveRequest(BaseModel):
    verified_root_cause: str
    verified_recovery_action: str


# Create a new incident
@router.post("/")
def create_incident(incident: IncidentCreate):
    try:
        db = connect_to_mongodb()

        incident_data = incident.model_dump()
        incident_data["status"] = "Open"
        incident_data["created_at"] = datetime.now(timezone.utc)

        result = db.incidents.insert_one(incident_data)

        return {
            "message": "Incident created successfully",
            "incident_id": str(result.inserted_id)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Retrieve all incidents
@router.get("/")
def get_incidents():
    try:
        db = connect_to_mongodb()

        incidents = list(
            db.incidents.find().sort("created_at", -1)
        )

        for incident in incidents:
            incident["_id"] = str(incident["_id"])
            incident["created_at"] = incident["created_at"].isoformat()

        return {
            "count": len(incidents),
            "incidents": incidents
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Search historical incidents using Hindsight
@router.post("/memory/search")
def search_incident_memory(request: MemorySearchRequest):
    try:
        result = recall_similar_incidents(
            query=request.query,
            limit=request.limit
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Resolve an incident and save verified findings in MongoDB
@router.patch("/{incident_id}/resolve")
def resolve_incident(
    incident_id: str,
    request: IncidentResolveRequest
):
    try:
        if not ObjectId.is_valid(incident_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid incident ID"
            )

        if not request.verified_root_cause.strip():
            raise HTTPException(
                status_code=400,
                detail="Verified root cause cannot be empty"
            )

        if not request.verified_recovery_action.strip():
            raise HTTPException(
                status_code=400,
                detail="Verified recovery action cannot be empty"
            )

        db = connect_to_mongodb()

        result = db.incidents.update_one(
            {
                "_id": ObjectId(incident_id),
                "status": "Open"
            },
            {
                "$set": {
                    "status": "Resolved",
                    "verified_root_cause": request.verified_root_cause,
                    "verified_recovery_action": request.verified_recovery_action,
                    "resolved_at": datetime.now(timezone.utc)
                }
            }
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Open incident not found"
            )

        return {
            "success": True,
            "message": "Incident resolved successfully",
            "incident_id": incident_id,
            "status": "Resolved"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Store a resolved incident in Hindsight Cloud
@router.post("/{incident_id}/memory/store")
def store_incident_memory(incident_id: str):
    try:
        if not ObjectId.is_valid(incident_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid incident ID"
            )

        db = connect_to_mongodb()

        incident = db.incidents.find_one({
            "_id": ObjectId(incident_id)
        })

        if not incident:
            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )

        result = store_resolved_incident(incident)

        return result

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Analyze an incident using Hindsight Cloud memories
@router.post("/{incident_id}/analyze")
def analyze_incident_endpoint(incident_id: str):
    try:
        if not ObjectId.is_valid(incident_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid incident ID"
            )

        db = connect_to_mongodb()

        incident = db.incidents.find_one({
            "_id": ObjectId(incident_id)
        })

        if not incident:
            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )

        # Search Hindsight for similar historical incidents
        memory_query = (
            f"{incident.get('service', '')} "
            f"{incident.get('title', '')} "
            f"{incident.get('description', '')}"
        )

        memory_result = recall_similar_incidents(
            query=memory_query,
            limit=5
        )

        historical_memories = memory_result.get(
            "memories", []
        )

        # Analyze current incident with retrieved memories
        analysis = analyze_incident(
            incident,
            historical_memories
        )

        return {
            "success": True,
            "incident_id": incident_id,
            "analysis": analysis
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
