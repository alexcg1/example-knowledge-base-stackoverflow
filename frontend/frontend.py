from jina import Client
from helper import (
    result_template,
    sidebar_text,
    get_rating,
    search_by_text,
    get_answers,
    html_to_markdown
)
from config import HOST
from docarray import Document
import streamlit as st

st.set_page_config(
    page_title="Jina Stack Overflow Knowledge Base Search",
    page_icon="🖱️",
    layout="wide",
)

st.header("🖱️ Jina Stack Overflow Knowledge Base Search")

st.sidebar.markdown(sidebar_text)

st.sidebar.markdown("### Options")

accepted_answers_only = st.sidebar.checkbox(label="Only show accepted answers")
# minimum_answer_score = st.sidebar.slider(label="Minimum answer score", min_value=-100, max_value=100)

user_input = st.text_input("What's your query?", "", key="input")

search_button = st.button("Search")

if search_button:
    results = search_by_text(user_input)

    for match in results:
        with st.expander(label=f"{match.tags['Score']} ⭐ | {match.text[:200]}"):
            st.markdown(f"### {match.text}")
            st.markdown(html_to_markdown(match.tags["Body"]))
            answers = get_answers(question_id=match.tags["Id"])
            st.markdown("#### Answers")
            for answer in answers:
                if accepted_answers_only:
                    if answer["IsAcceptedAnswer"] == "True":
                        st.markdown(html_to_markdown(answer["Body"]))
                        st.markdown(
                            f"**Score:** {answer['Score']} | **Accepted**: {answer['IsAcceptedAnswer']}"
                        )
                        st.markdown("---")

                else:
                    st.markdown(html_to_markdown(answer["Body"]))
                    st.markdown(
                        f"**Score:** {answer['Score']} | **Accepted**: {answer['IsAcceptedAnswer']}"
                    )
                    st.markdown("---")
