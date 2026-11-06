

def analyze_incident(incident, historical_memories=None):
    """
    Analyze an incident using its details and memories
    retrieved from Hindsight Cloud.

    This version uses rule-based reasoning, not Grok.
    """

    historical_memories = historical_memories or []

    service = incident.get("service", "Unknown service")
    severity = incident.get("severity", "SEV-4")
    title = incident.get("title", "")
    description = incident.get("description", "")

    incident_text = f"{title} {description}".lower()

    probable_causes = []

    if any(word in incident_text for word in ["timeout", "slow", "latency"]):
        probable_causes.extend([
            "Possible database or dependency latency",
            "Possible resource exhaustion",
            "Possible network connectivity problems"
        ])

    if any(word in incident_text for word in ["error", "failure", "crash"]):
        probable_causes.extend([
            "Possible application failure",
            "Possible dependency failure"
        ])

    if not probable_causes:
        probable_causes.append(
            "Insufficient evidence to identify a probable cause"
        )

    investigation_steps = [
        f"Inspect application logs for {service}.",
        "Check CPU and memory utilization.",
        "Review recent deployments and configuration changes.",
        "Check database and external dependency health."
    ]

    return {
        "analysis_type": "RULE_BASED_WITH_HINDSIGHT",
        "is_simulated": True,
        "incident_summary": f"{service}: {description}",
        "severity": severity,
        "probable_root_causes": probable_causes,
        "investigation_steps": investigation_steps,
        "historical_memory_count": len(historical_memories),
        "historical_memories": historical_memories,
        "verified_root_cause": None,
        "confidence": "Not assessed"
    }
