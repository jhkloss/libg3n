import glob
import libg3n
from abc import ABC, abstractmethod
from .libg3n_file import Libg3nFile


class Libg3nLibrary(ABC):
    """
    Abstract class representing an Libg3n library. Encapsulate functions to find and manage library files.
    """

    # Path pointing to the library root
    _path: str

    # List of found files
    _files = []

    # Number of files found
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
        """
        Abstract property defining the file extension for library files.
        """
        pass

    @abstractmethod
    def index_file(self, path: str) -> Libg3nFile:
        pass

    def scan(self):
        """
        Scans the library for files matching the file extension for library files.
        """
        libg3n.logger.debug('Started library scan')
        for file in glob.iglob(self._path + '/**/*.' + self.file_extension, recursive=True):
            current_file = self.index_file(file)
            self._files.append(current_file)
            self._number_of_files += 1
