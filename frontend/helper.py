from docarray import Document
from jina import Client
from config import HOST, DATABASE_FILE, REPO_URL

result_template = """### {title}

**Source**: [{source}]({url})

{text}"""

sidebar_text = f"# Introduction\n\nThis search engine is built using: \n\n - [**DocArray**](https://docarray.jina.ai): The data structure for unstructured data\n- [**Jina**](https://github.com/jina-ai/jina/): Cloud native neural search framework\n- [**JCloud**](https://github.com/jina-ai/jcloud/) -  Simplify deploying and managing Jina projects on Jina Cloud \n- [**Streamlit**](https://streamlit.io/) - frontend\n## Useful links\n\n- [Code repository]({REPO_URL})\n - [Stack OverFlow R Questions](https://www.kaggle.com/datasets/stackoverflow/rquestions)"


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

def get_answers(question_id, db_file=DATABASE_FILE, table_name="Answers", id_field="ParentId"):
    import sqlite3 as db

    conn = db.connect(db_file)
    sql = f"SELECT * FROM {table_name} WHERE {id_field} = {question_id}"
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    answers = []

    for row in rows:
        answer = {
            "Body": row[6],
            "Score": row[4],
            "IsAcceptedAnswer": row[5]
        }
        answers.append(answer)

    return answers

def html_to_markdown(html, code_language="r"):
    from markdownify import markdownify
    markdown = markdownify(html, heading_style="ATX", code_language=code_language)

    return markdown
