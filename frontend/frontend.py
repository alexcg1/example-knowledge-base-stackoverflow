from jina import Client
from helper import result_template, sidebar_text, get_rating
from config import HOST
from docarray import Document
import streamlit as st

st.set_page_config(page_title="Jina COVID-19 Knowledge Base Search", page_icon=":book:")

st.header("🔖 Jina COVID-19 Knowledge Base Search")

st.sidebar.markdown(sidebar_text)


def search_by_text(input, server=HOST):
    client = Client(host=server)
    response = client.search(
        Document(text=input),
        # parameters={"limit": limit},
        return_results=True,
    )
    matches = response[0].matches

    return matches


user_input = st.text_input("What's your query?", "", key="input")

search_button = st.button("Search")

if search_button:
    results = search_by_text(user_input)

    for match in results:
        rating_icon = get_rating(match.tags["answer_type"])
        with st.expander(label=f"{rating_icon} {match.tags['answer'][:200]}"):
            st.markdown(
                result_template.format(
                    title=match.text,
                    text=match.tags["answer"],
                    source=match.tags["source"],
                    url=match.tags["url"]
                )
            )
