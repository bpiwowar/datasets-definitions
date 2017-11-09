import logging
from datasets.data import Handler, DownloadHandler

class Sgml(Handler):
    def download(self):
        # Verify if the dataset has been downloaded
        print(self.dataset)
        raise Exception("Not implemented")