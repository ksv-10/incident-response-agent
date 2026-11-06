from app.core.hindsight_client import (
    get_hindsight_client,
    get_memory_bank_id
)

client = get_hindsight_client()
bank_id = get_memory_bank_id()

try:
    bank = client.create_bank(
        bank_id=bank_id,
        name="Incident Response Agent",
        reflect_mission=(
            "Help an SRE incident response agent retrieve "
            "relevant historical incidents, verified causes, "
            "recovery actions, and lessons learned. "
            "Distinguish confirmed facts from hypotheses."
        )
    )

    print("Hindsight memory bank created successfully!")
    print("Bank ID:", bank_id)

finally:
    client.close()