from datasets.handlers.datasets import DatasetHandler
from .documents import DocumentList

class Warc(DocumentList):
    def prepare(self):
        r = super().prepare()
        r["$type"] = "datasets.web.warc"
        return r