from docarray import DocumentArray, Document
from jina import Flow, Client
from config import DATA_FILE, NUM_DOCS, HOST, TEXT_FIELD
# from executor import HtmlStripper
import click

flow = Flow.load_config("flow.yml")


def index_local(num_docs=NUM_DOCS):
    flow = Flow.load_config("flow-local.yml")
    docs = DocumentArray.from_csv(
        DATA_FILE, field_resolver={TEXT_FIELD: "text"}, size=num_docs
    )

    with flow:
        docs = flow.index(docs, show_progress=True)
    # for doc in docs:
        # print(doc.text)
        # print(doc.tags)

        # for chunk in doc.chunks:
            # print(chunk.text)




def index(num_docs=NUM_DOCS):
    docs = DocumentArray.from_csv(
        DATA_FILE, field_resolver={TEXT_FIELD: "text"}, size=num_docs
    )
    client = Client(host=HOST)
    client.index(docs, show_progress=True)


def search_grpc():
    flow = Flow.load_config("flow-local.yml")
    while True:
        query = input("What's your query? ")
        doc = Document(text=query)
        with flow:
            results = flow.search(doc)

        # print(results[0].matches)

        for match in results[0].matches:
            print(match.text)
            print("---")


def search():
    flow = Flow.load_config("flow-local.yml")
    with flow:
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search", "index_local", "search_grpc"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=NUM_DOCS)
def main(task: str, num_docs):
    if task == "index":
        index(num_docs=num_docs)
    elif task == "index_local":
        index_local(num_docs=num_docs)
    elif task == "search":
        search()
    elif task == "search_grpc":
        search_grpc()
    else:
        print("Please add '-t index' or '-t search' to your command")


if __name__ == "__main__":
    main()
