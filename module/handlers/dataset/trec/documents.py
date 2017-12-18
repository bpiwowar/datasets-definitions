import logging
from datasets.handlers.datasets import DatasetHandler
from ..documents import DocumentList

class Sgml(DocumentList):
    def prepare(self):
        r = super().prepare()
        r["$type"] = "ds.gov.nist.tipster"
        return r