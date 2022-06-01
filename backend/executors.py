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


def test():
    doc = Document(tags={"CreationDate": "2009-07-12T15:18:02Z"})
    docs = DocumentArray([doc])

    flow = Flow().add(uses=DateTimeStringToFloat, uses_with={"tags": ["CreationDate"]})

    with flow:
        response = flow.index(docs)

    print([doc.tags for doc in response])


if __name__ == "__main__":
    test()
