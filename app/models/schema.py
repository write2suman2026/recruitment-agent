from typing import TypedDict

class AgentState(TypedDict):
    resume_text: str
    jd_text: str

    candidate_json: dict
    jd_json: dict

    score_json: dict
    explanation: str