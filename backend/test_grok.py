from app.core.ai_client import get_xai_client
from openai import APIStatusError

client = get_xai_client()

try:
    response = client.chat.completions.create(
        model="grok-4.7",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant specialized in site reliability engineering."
            },
            {
                "role": "user",
                "content": "Explain what a SEV-1 production incident means in two sentences."
            }
        ]
    )

    print("\nGrok Response:\n")
    print(response.choices[0].message.content)

except APIStatusError as e:
    print("API Status:", e.status_code)
    print("Error Details:", e.response.text)

except Exception as e:
    print("Error:", str(e))