from utils.llm_client import client


def explain_agent(state):

    prompt = f"""
Explain the candidate match.

Score:

{state['score_json']}

Candidate:

{state['candidate_json']}

Job Description:

{state['jd_json']}

Provide:

1. Overall assessment
2. Strengths
3. Missing skills
4. Recommendation

Keep it under 200 words.
"""

    response = client.invoke(prompt)

    state["explanation"] = response.content

    return state