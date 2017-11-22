import logging
from datasets.handlers.datasets import DatasetHandler
from ..documents import DocumentList

class Sgml(DocumentList):
    def prepare(self):
        r = super().prepare()
        r["$type"] = "tipster.sgml"
        return r