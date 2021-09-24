from abc import ABC, abstractmethod
from .libg3n_file import Libg3nFile

class Libg3nLibrary(ABC):
    _files = []
    _path: str
    _number_of_files: int = 0

    def __init__(self, path: str):
        self._path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: str):
        self._path = path

    @property
    def files(self):
        return self._files

    @property
    def number_of_files(self):
        return self._number_of_files

    @property
    @abstractmethod
    def file_extension(self):
        pass

    @abstractmethod
    def index_file(self, path: str) -> Libg3nFile:
        pass

    def scan(self):
        libg3n.logger.debug('Started library scan')
        for file in glob.iglob(self.__path + '/**/*.' + self.file_extension, recursive=True):
            current_file = self.index_file(file)
            self.__files.append(current_file)
            self.__number_of_files += 1
