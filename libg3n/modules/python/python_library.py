from libg3n.model.libg3n_library import Libg3nLibrary
from libg3n.model.libg3n_file import Libg3nFile
from .python_file import PythonFile


class PythonLibrary(Libg3nLibrary):

    @property
    def file_extension(self):
        return 'py'

    def index_file(self, path: str) -> Libg3nFile:
        return PythonFile(path)