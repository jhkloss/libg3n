from abc import ABC, abstractmethod, abstractproperty
from os.path import exists, basename, splitext

from libg3n.model.libg3n_config import Libg3nConfig


class Libg3nFile(ABC):
    _path: str
    _tree: any
    _code: str
    _touched: bool = False
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
    def tree(self):
        return self._tree

    @tree.setter
    def tree(self, tree: any):
        self._tree = tree

    @property
    def code(self):
        return self._code

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: str):
        self._encoding = encoding

    @property
    @abstractmethod
    def file_extension(self) -> str:
        pass

    @property
    def file_name(self):
        name_with_ext = basename(self._path)
        return splitext(name_with_ext)

    def touch(self):
        self._touched = True

    def touched(self):
        return self._touched

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def process(self, config: Libg3nConfig):
        pass

    @abstractmethod
    def unparse(self) -> str:
        pass

    def read(self) -> str:
        file_content = ""

        if exists(self._path):
            with open(self._path, encoding=self._encoding) as f:
                file_content = f.read()

        return file_content

    def write(self, file_path: str, file_name: str = "", encoding: str = ""):

        if not encoding:
            encoding = self._encoding

        if not file_name:
            file_name = self.file_name

        with open(file_path + file_name + '.' + self.file_extension, 'w', encoding=encoding) as f:
            f.write(self._code)
