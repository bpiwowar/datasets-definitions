import logging
from datasets.data import Handler, DownloadHandler

class Collection(Handler):
    """Just a set of document collections"""
    def download(self):
        for ref in self.content["references"]:
            ref.download()
        # Verify if the dataset has been downloaded
        return False

    def __repr__(self):
        return "Collection(%s)" % (", ".join([repr(r) for r in self.content["references"]]))
