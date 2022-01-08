from abc import ABC, abstractmethod
from os.path import exists

from libg3n.model.libg3n_function import FunctionType


class Libg3nConfigParser(ABC):

    _path = ''
    _config = ''

    FUNCTION_DICT_KEY = 'functions'
    CLASS_DICT_KEY = 'class'

    FUNCTION_TYPES = {
        'return': FunctionType.RETURN,
        'custom': FunctionType.CUSTOM,
        'external': FunctionType.EXTERNAL,
    }

    def _load_file(self, path):
        self._path = path

        if exists(path):
            with open(path) as f:
                self._config = f.read()

    def _parse_function_type(self, function_type_str: str) -> FunctionType:
        return self.FUNCTION_TYPES[function_type_str]

    @abstractmethod
    def parse(self, path: str) -> dict:
        pass

