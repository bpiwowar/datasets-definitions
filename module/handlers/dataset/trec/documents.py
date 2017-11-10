import logging
from datasets.data import Handler, DownloadHandler

class Sgml(Handler):
    def download(self):
        # Verify if the dataset has been downloaded
        basedir = self.config.datapath.joinpath(*self.dataset.id.split("."))
        path = self.datapath.with_suffix(".relfiles")

        with open(path, "rt") as fp:
            for line in fp:
                path = basedir.joinpath(line.strip())
                if not path.is_file():
                    print("%s is not a file" % path)

        raise Exception("Not implemented")