from libg3n.model.libg3n_file import Libg3nFile
from libg3n.model.libg3n_config import Libg3nConfig
from libg3n.modules.java.java_regex_parser import JavaRegexParser


class JavaFile(Libg3nFile):

    _regex_parser = JavaRegexParser()

    @property
    def file_extension(self) -> str:
        return 'java'

    def parse(self):
        self._regex_parser.parse_file(self.path)

    def process(self, config: Libg3nConfig):
        pass

    def unparse(self) -> str:
        pass