from abc import ABC, abstractmethod, abstractproperty
from os.path import exists, basename, splitext

import libg3n
from libg3n.exception.EmptyFileException import EmptyFileException
from libg3n.exception.InvalidFileException import InvalidFileException
from libg3n.model.libg3n_config import Libg3nConfig


class Libg3nFile(ABC):
    """
    Abstract class representing a scanned file inside the given library. Provides functions to read, analyse and alter
    the content of the representing file.
    """

    # Path to the actual file
    _path: str

    # Read code from the file
    _code: str = ''

    # Boolean value specifying if this file is altered and needs to be generated
    _touched: bool = False

    # Encoding of the file
    _encoding: str = 'utf-8'

    def __init__(self, path: str):
        self._path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        self._code = code

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: str):
        self._encoding = encoding

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """
        Abstract property. File extension of the file.
        """
        pass

    @property
    def file_name(self):
        name_with_ext = basename(self._path)
        return splitext(name_with_ext)[0]

    def touch(self):
        """
        Touches this file and mark it for generation.
        """
        self._touched = True

    def touched(self):
        return self._touched

    @abstractmethod
    def parse(self):
        """
        Abstract method which specifies how this file can be parsed in dependence of the used programming language.
        """
        pass

    @abstractmethod
    def process(self, config: Libg3nConfig):
        """
        Abstract method which specifies how this file is scanned for generation markers in dependence of the used
        programming language.
        """
        pass

    @abstractmethod
    def unparse(self) -> str:
        """
        Abstract method which specifies how this file is unparsed and generation markers a treated in dependence of the
        used programming language.
        """
        pass

    def read(self) -> str:
        """
        Reads the file contents.
        """
        if exists(self._path):
            with open(self._path, encoding=self._encoding) as f:
                file_content = f.read()

                if file_content:
                    self._code = file_content
                    return file_content
                else:
                    raise EmptyFileException()
        else:
            raise InvalidFileException()


def write(self, file_path: str, file_name: str = "", encoding: str = ""):
    """
    Writes the code back to a file.
    """
    libg3n.logger.debug('Writing file: ' + file_path + file_name + '.' + self.file_extension)

    if not encoding:
        encoding = self._encoding

    if not file_name:
        file_name = self.file_name

    # Make sure the current sourcecode was unparsed.
    if not self._code:
        self._code = self.unparse()

    # Make sure the sourcecode is valid before it is written
    if self._code:
        # Write the sourcecode to a new file.
        with open(file_path + file_name + '.' + self.file_extension, 'w', encoding=encoding) as f:
            f.write(self._code)
