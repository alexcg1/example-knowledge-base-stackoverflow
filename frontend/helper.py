from docarray import Document
from jina import Client
from config import HOST

result_template = """### {title}

**Source**: [{source}]({url})

{text}"""

sidebar_text = "# Introduction\n\nThis search engine is built using: \n\n - [**DocArray**](https://docarray.jina.ai): The data structure for unstructured data\n- [**Jina**](https://github.com/jina-ai/jina/): Cloud native neural search framework\n- [**JCloud**](https://github.com/jina-ai/jcloud/) -  Simplify deploying and managing Jina projects on Jina Cloud \n- [**Streamlit**](https://streamlit.io/) - frontend\n## Useful links\n\n- [Code repository](https://github.com/alexcg1/example-knowledge-base-search)\n - [Stack OverFlow R Questions](https://www.kaggle.com/datasets/stackoverflow/rquestions)"


def get_rating(status):
    if status == True:
        return "🟢"
    else:
        return "🔴"


def search_by_text(input, server=HOST):
    client = Client(host=server)
    response = client.search(
        Document(text=input),
        parameters={"traversal_path": "@r"},
    )
    matches = response[0].matches

    return matches
