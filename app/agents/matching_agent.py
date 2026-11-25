def matching_agent(state):

    candidate=state["candidate_json"]

    jd=state["jd_json"]

    skills=set(
        [x.lower() for x in candidate["skills"]]
    )

    mandatory=set(
        [x.lower() for x in jd["mandatory_skills"]]
    )

    matched = skills.intersection(mandatory)

    skill_score = (
        len(matched)
        / max(len(mandatory),1)
    ) * 70

    exp_score=0

    if candidate["experience_years"] >= jd["experience_years"]:
        exp_score=20

    cert_score=10

    total=round(
        skill_score+exp_score+cert_score,
        2
    )

    state["score_json"] = {
        "overall_score": total,
        "matched_skills": list(matched),
        "missing_skills": list(
            mandatory-matched
        )
    }

    return state