from docarray import DocumentArray, Document
from jina import Flow, Client
from config import DATA_FILE, NUM_DOCS, HOST, TEXT_FIELD
import click


def index(cloud: bool, num_docs: int = NUM_DOCS):
    print(f"Processing {num_docs} Documents")
    docs = DocumentArray.from_csv(
        DATA_FILE, field_resolver={TEXT_FIELD: "text"}, size=num_docs
    )
    if cloud:
        client = Client(host=HOST)
        client.post(
            "/update", docs, show_progress=True, parameters={"traversal_path": "@r"}
        )
    else:
        flow = Flow.load_config("flows/flow-local.yml")
        with flow:
            docs = flow.index(
                docs, show_progress=True, parameters={"traversal_path": "@r"}
            )


def search_grpc():
    flow = Flow.load_config("flows/flow-local.yml")
    while True:
        query = input("What's your query? ")
        doc = Document(text=query)
        with flow:
            results = flow.search(doc, parameters={"traversal_path": "@r"})

        for match in results[0].matches:
            print(match.text)
            print(match.tags)
            print("---")


def serve():
    flow = Flow.load_config("flows/flow-local.yml")
    with flow:
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "serve", "search_grpc"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=NUM_DOCS)
@click.option("--cloud", "-c", is_flag=True)
def main(task: str, num_docs: int, cloud: bool):
    if task == "index":
        index(cloud, num_docs=num_docs)
    elif task == "serve":
        serve()
    elif task == "search_grpc":
        search_grpc()
    else:
        print("Please add '-t index' or '-t search' to your command")


if __name__ == "__main__":
    main()
