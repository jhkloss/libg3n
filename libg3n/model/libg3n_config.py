from abc import ABC, abstractmethod


class Libg3nConfig(ABC):
    _path: str
    _functions = {}
    _classes = {}

    def __init__(self, path):
        self._path = path
        self.parser.load_file(path)
        self._functions = self.parser.get_functions()
        self._classes = self.parser.get_classes()

    @property
    def functions(self):
        return self._functions

    @property
    def classes(self):
        return self._classes

    @property
    @abstractmethod
    def parser(self):
        pass
