from abc import ABC, abstractmethod

import libg3n
from libg3n.model.libg3n_config_parser import Libg3nConfigParser


class Libg3nConfig(ABC):
    """
    Represents a Libg3n config, providing the original config file path and the parsed functions and classes.
    """

    # Path to the config file
    _path: str

    # Parsed functions
    _functions = {}

    # Parsed classes
    _classes = {}

    def __init__(self, path):
        # Preserve Path
        self._path = path

        # Use the parser to parse the file and extract functions and classes from it
        token_dict = self.parser.parse(path)

        # Save the parsed result, seperated into functions and classes
        self._functions = token_dict[self.parser.FUNCTION_DICT_KEY]
        self._classes = token_dict[self.parser.CLASS_DICT_KEY]

    @property
    def functions(self):
        return self._functions

    @property
    def classes(self):
        return self._classes

    @property
    @abstractmethod
    def parser(self) -> Libg3nConfigParser:
        """
        Abstract class defining the module / language specific config parser.
        """
        pass
