import tempfile

import streamlit as st

from utils.pdf_reader import extract_text
from graph.workflow import build_graph

graph=build_graph()

st.title(
    "AI Recruitment Matching POC"
)

resume=st.file_uploader(
    "Upload Resume"
)

jd=st.text_area(
    "Paste Job Description"
)

if st.button("Evaluate"):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:

        tmp.write(resume.read())

        resume_text=extract_text(
            tmp.name
        )

    result=graph.invoke(
        {
            "resume_text":resume_text,
            "jd_text":jd
        }
    )

    st.metric(
        "Match %",
        result["score_json"]["overall_score"]
    )

    st.json(
        result["score_json"]
    )

    st.write(
        result["explanation"]
    )