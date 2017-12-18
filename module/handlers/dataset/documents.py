import logging
from itertools import chain
from datasets.handlers.datasets import DatasetHandler
from datasets.context import Compression

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
        return { "id": self.dataset.id, "$type": "ds.collection", "list": l }

    def __repr__(self):
        return "Collection(%s)" % (", ".join([repr(r) for r in self.content["references"]]))


class DocumentList(DatasetHandler):
    """Documents associated with a list of files"""
    def documents(self):
        # Get extension
        registry = self.context.registry[self.dataset.id]
        extension = Compression.extension(registry.get("compression", None))

        # Get list of files
        path = self.extrapath.with_suffix(".relfiles")
        basedir = self.dataset.datadir

        with open(path, "rt") as fp:
            for line in fp:
                path = basedir.joinpath(line.strip())
                if extension:
                    path = path.with_suffix(path.suffix + extension)
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

        return { "id": self.dataset.id, "path": gpath }
