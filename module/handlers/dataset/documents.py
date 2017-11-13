import logging
from itertools import chain
from datasets.handlers.datasets import DatasetHandler

class Collection(DatasetHandler):
    """Just a set of document collections"""
    def download(self):
        success = True
        for ref in self.content["references"]:
            success = ref.download() & success
        return success

    def documents(self):
        """Returns the list of files with their characteristics"""
        return chain(*[r.documents() for r in self.content["references"]])
            
    def prepare(self):
        l = []
        for r in self.content["references"]:
            l.append(r.prepare())
        return { "id": self.dataset.id, "type": "collection", "list": l }

    def __repr__(self):
        return "Collection(%s)" % (", ".join([repr(r) for r in self.content["references"]]))
