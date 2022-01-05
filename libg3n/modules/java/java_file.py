from libg3n.model.libg3n_file import Libg3nFile
from libg3n.model.libg3n_config import Libg3nConfig
from libg3n.modules.java.java_regex_parser import JavaRegexParser


class JavaFile(Libg3nFile):

    _regex_parser = JavaRegexParser()
    _parsed_functions = None
    _function_matches = {}
    _offset = 0

    @property
    def file_extension(self) -> str:
        return 'java'

    def parse(self):
        self._parsed_functions = self._regex_parser.parse_file(self.path)

    def process(self, config: Libg3nConfig):

        for function in self._parsed_functions:
            for config_function in config.functions:
                if config_function.matches(function, self._regex_parser.GroupNames.IDENT):
                    config_function.match = function
                    # self._function_matches[config_function.ident] = {'function': function, 'config': config_function}

    def unparse(self) -> str:
        self._offset = 0
        result = self._code

        # Iterate over the matched functions
        for function in self._parsed_functions:

            # Generate the function code segment
            function_code = function.generate_body

            # Insert the code into the original sourcecode
            result = self._insert_between(result, function_code, function.start_line, function.end_line)

        return result

    def _insert_between(self, source: str, payload: str, start: int, end: int) -> str:

        # Preserve original length
        length = len(source)

        # Insert the payload code
        result = source[0:start+self._offset] + payload + source[end+self._offset:length]

        # Compare lengths and add new offset
        self._offset += length - len(result)

        # Return the resulting sourcecode
        return result
