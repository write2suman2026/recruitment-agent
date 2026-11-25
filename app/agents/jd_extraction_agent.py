import json

from utils.json_parser import extract_json
from utils.llm_client import client


def jd_agent(state):

    prompt = f"""
Extract:

1. Mandatory skills
2. Experience years
3. Certifications

Job Description:

{state['jd_text']}

Return ONLY valid JSON in this format:

{{
    "mandatory_skills": [],
    "experience_years": 0,
    "certifications": []
}}
"""

    response = client.invoke(prompt)

    state["jd_json"] = extract_json(response.content)

    return state
