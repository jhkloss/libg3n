from libg3n.model.libg3n_config import Libg3nConfig
from libg3n.modules.python.python_config_parser import PythonConfigParser

class PythonConfig(Libg3nConfig):

    _parser = PythonConfigParser()

    @property
    def parser(self):
        return _parser