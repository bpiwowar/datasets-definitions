import logging
from datasets.handlers.datasets import DatasetHandler
from datasets.data import Compression

class Sgml(DatasetHandler):
    def documents(self):
        # Get extension
        registry = self.config.registry[self.dataset.id]
        extension = Compression.extension(registry["compression"])

        # Get list of files
        path = self.extrapath.with_suffix(".relfiles")
        basedir = self.dataset.datadir

        with open(path, "rt") as fp:
            for line in fp:
                path = basedir.joinpath(line.strip())
                if extension:
                    path = path.with_suffix(extension)
                yield path

    def download(self):   
        count = 0
        for path in self.documents():
            if not path.is_file():
                count += 1
                logging.debug("%s is not a file" % path)

        if count:
            logging.error("%d files were not for SGML document collection %s. Place them in %s", count, self.dataset.id, self.dataset.datadir)

        return count == 0

    def prepare(self):
        gpath = self.generatedpath.with_suffix(".lst")
        logging.info("Generating %s", gpath)
        gpath.parent.mkdir(parents=True, exist_ok=True)
        with open(gpath, "wt") as out:
            for path in self.documents():
                out.write(str(path.resolve()))
                out.write('\n')

        return { "id": self.dataset.id, "path": gpath, "type": "tipster/sgml" }