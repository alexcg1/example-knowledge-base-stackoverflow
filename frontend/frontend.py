from jina import Client
from helper import result_template, sidebar_text, get_rating, search_by_text
from config import HOST
from docarray import Document
import streamlit as st

st.set_page_config(page_title="Jina Stack Overflow Knowledge Base Search", page_icon=":book:", layout="wide")

st.header("🔖 Jina Stack Overflow Knowledge Base Search")

st.sidebar.markdown(sidebar_text)

user_input = st.text_input("What's your query?", "", key="input")

search_button = st.button("Search")

if search_button:
    results = search_by_text(user_input)

    for match in results:
        rating_icon = get_rating(match.tags["IsAcceptedAnswer"])
        with st.expander(label=f"{rating_icon} {match.text[:200]}"):
            st.markdown(
                f"{match.text}\n---\n{match.tags['Score']} ⭐"

                # result_template.format(
                    # title=match.text,
                    # text=match.tags["answer"],
                    # source=match.tags["source"],
                    # url=match.tags["url"]
                # )
            )
