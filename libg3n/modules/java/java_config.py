from libg3n.model.libg3n_config import Libg3nConfig
from libg3n.modules.java.java_config_parser import JavaConfigParser


class JavaConfig(Libg3nConfig):

    _parser = JavaConfigParser()

    @property
    def parser(self):
        return self._parser
