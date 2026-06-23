import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def roast_resume(resume_text: str):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a funny but helpful career coach.

Analyze this resume and return:
1. Funny roast
2. Skill gaps
3. Job readiness score (0–100)
4. Improvement suggestions

Resume:
{resume_text}
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()