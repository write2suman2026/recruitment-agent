def bias_agent(state):

    candidate=state["candidate_json"]

    protected_fields = [
        "gender",
        "age",
        "date_of_birth",
        "religion",
        "nationality",
        "marital_status"
    ]

    for field in protected_fields:
        candidate.pop(field,None)

    state["candidate_json"]=candidate

    return state