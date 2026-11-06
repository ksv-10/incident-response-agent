
from app.core.hindsight_client import (
    get_hindsight_client,
    get_memory_bank_id
)


def store_resolved_incident(incident):
    """
    Store a resolved incident in Hindsight Cloud.
    Only verified incident information is retained.
    """

    if incident.get("status") != "Resolved":
        raise ValueError(
            "Only resolved incidents can be stored in long-term memory."
        )

    incident_id = str(incident.get("_id", "unknown"))

    required_fields = [
        "title",
        "service",
        "severity",
        "description"
    ]

    for field in required_fields:
        if not incident.get(field):
            raise ValueError(
                f"Missing required incident field: {field}"
            )

    root_cause = incident.get("verified_root_cause")
    recovery = incident.get("verified_recovery_action")

    if not root_cause or not recovery:
        raise ValueError(
            "Verified root cause and recovery action are required."
        )

    content = f"""
RESOLVED INCIDENT

Incident ID: {incident_id}
Title: {incident['title']}
Service: {incident['service']}
Severity: {incident['severity']}

Description:
{incident['description']}

Verified root cause:
{root_cause}

Verified recovery action:
{recovery}

Status: Resolved
"""

    client = get_hindsight_client()

    try:
        result = client.retain(
            bank_id=get_memory_bank_id(),
            content=content,
            context="Verified production incident and lessons learned",
            metadata={
                "incident_id": incident_id,
                "service": incident["service"],
                "severity": incident["severity"],
                "status": "Resolved",
                "source": "MongoDB"
            }
        )

        return {
            "success": True,
            "incident_id": incident_id,
            "message": "Incident submitted to Hindsight memory.",
            "result": str(result)
        }

    finally:
        client.close()


def recall_similar_incidents(query, limit=5):
    """
    Retrieve relevant historical incident memories from Hindsight.
    """

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    client = get_hindsight_client()

    try:
        result = client.recall(
            bank_id=get_memory_bank_id(),
            query=query,
            budget="low"
        )

        memories = []

        for memory in result.results[:limit]:
            memories.append({
                "type": memory.type,
                "content": memory.text
            })

        return {
            "success": True,
            "query": query,
            "count": len(memories),
            "memories": memories
        }

    finally:
        client.close()
