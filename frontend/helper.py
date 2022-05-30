result_template = """### {title}

**Source**: [{source}]({url})

{text}"""

sidebar_text = "# Introduction\n\nThis chatbot is built using: \n\n - [**DocArray**](https://docarray.jina.ai): The data structure for unstructured data\n- [**Jina**](https://github.com/jina-ai/jina/): Cloud native neural search framework\n- [**JCloud**](https://github.com/jina-ai/jcloud/) -  Simplify deploying and managing Jina projects on Jina Cloud \n- [**Streamlit**](https://streamlit.io/) - frontend\n## Useful links\n\n- [Code repository](https://github.com/alexcg1/example-chatbot)\n - [COVID-QA dataset from Kaggle](https://www.kaggle.com/xhlulu/covidqa/)\n\n## Disclaimer\n\nThis app is intended only as a technical demonstration. **DO NOT TAKE MEDICAL ADVICE FROM STRANGE APPS ON THE INTERNET** (especially ones with outdated datasets)"


def get_rating(rating_text):
    if rating_text == "Accepted":
        return "🟢"
    elif rating_text == "Reasonable":
        return "🟠"
    else:
        return "🔴"
