from libg3n.model.libg3n_file import Libg3nFile
from libg3n.model.libg3n_library import Libg3nLibrary
from libg3n.modules.java.java_file import JavaFile


class JavaLibrary(Libg3nLibrary):

    @property
    def file_extension(self):
        return 'java'

    def index_file(self, path: str) -> Libg3nFile:
        return JavaFile(path)
