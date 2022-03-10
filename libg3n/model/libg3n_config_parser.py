from abc import ABC, abstractmethod
from os.path import exists

from libg3n.model.libg3n_function import FunctionType
from libg3n.exception.InvalidFileException import InvalidFileException


class Libg3nConfigParser(ABC):
    """
    Abstract class representing a Libg3n config parser. Used to parse different config file formats and extract
    functions and classes from it.
    """

    # Config file path
    _path = ''

    # Unparsed config contents
    _config = ''

    # Dict Key for storing functions
    FUNCTION_DICT_KEY = 'functions'

    # Dict Key for storing classes
    CLASS_DICT_KEY = 'class'

    # Valid function types
    FUNCTION_TYPES = {
        'return': FunctionType.RETURN,
        'custom': FunctionType.CUSTOM,
        'external': FunctionType.EXTERNAL,
    }

    def _load_file(self, path):
        """
        Loads a file and stores its content in the _config class variable.
        """
        self._path = path

        if exists(path):
            with open(path) as f:
                self._config = f.read()
        else:
            raise InvalidFileException(path, "Configuration")

    def _parse_function_type(self, function_type_str: str) -> FunctionType:
        """
        Parses the given function Type string by matching it with the FUNCTION_TYPES dict.
        """
        return self.FUNCTION_TYPES[function_type_str]

    @abstractmethod
    def parse(self, path: str) -> dict:
        """
        Abstract method which specifies the way how functions and classes are extracted from the corresponding config
        file format.
        """
        pass

