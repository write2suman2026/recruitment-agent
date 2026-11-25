import json

from utils.llm_client import client


from utils.json_parser import extract_json

def resume_agent(state):

    prompt = f"""
Extract candidate profile.

Resume:

{state['resume_text']}

Return ONLY valid JSON:

{{
    "name": "",
    "skills": [],
    "experience_years": 0,
    "certifications": []
}}
"""

    response = client.invoke(prompt)


    state["candidate_json"] = extract_json(response.content)

    return state