from docarray import Document, DocumentArray
from jina import Executor, requests, Flow
from datetime import datetime

field_name = "CreationDate"

class DateTimeStringToFloat(Executor):
    def __init__(self, tags, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = tags

    @requests
    def convert_date_time_string_to_float(self, docs, **kwargs):
        print(self.tags)
        for doc in docs:
            for tag in self.tags:
                datetime_str = doc.tags[tag][:10]
                datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d")
                datetime_float = datetime_obj.timestamp()
                doc.tags[tag] = datetime_float


class ParentToChunkTag(Executor):
    def __init__(self, traversal_paths: str = "@r", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.traversal_paths = traversal_paths

    @requests(on="/index")
    def embed_parent_text_in_chunk_tag(self, docs, parameters, **kwargs):
        traversal_paths = parameters.get("traversal_paths", self.traversal_paths)
        for doc in docs[traversal_paths]:
            print(doc.text)
            print(doc.parent_id)
            # print(doc.parent_id)
            # for chunk in doc.chunks:
                # print(chunk.parent_id)
                # print(docs[chunk.parent_id].text)

            if doc.parent_id:
                doc.tags["parent_content"] = docs[doc.parent_id].text
            # print(dir(doc))



def test():
    doc = Document(tags={"CreationDate": "2009-07-12T15:18:02Z"})
    docs = DocumentArray([doc])

    flow = Flow().add(uses=DateTimeStringToFloat, uses_with={"tags": ["CreationDate"]})

    with flow:
        response = flow.index(docs)

    print([doc.tags for doc in response])

def test_chunktag():
    from docarray import Document, DocumentArray

    docs = DocumentArray(
        [
            Document(
                text="foo",
                chunks=DocumentArray([Document(text="bar"), Document(text="baz")]),
            ),
            Document(
                text="thing",
                chunks=DocumentArray([Document(text="bar"), Document(text="baz")]),
            ),
            Document(
                text="plonk",
                chunks=DocumentArray([Document(text="bar"), Document(text="baz")]),
            ),
        ]
    )

    for doc in docs:
        for chunk in doc.chunks:
            print(chunk.text)
            print(chunk.parent_id)

    flow = Flow().add(uses=ParentToChunkTag, parameters={"traversal_paths": "@c"})

    with flow:
        output = flow.index(docs)

    for doc in output:
        # print(dir(doc))
        print(doc.chunks[0].tags)


if __name__ == "__main__":
    test_chunktag()
