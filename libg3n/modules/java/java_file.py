from libg3n.model.libg3n_file import Libg3nFile
from libg3n.model.libg3n_config import Libg3nConfig
from libg3n.modules.java.java_regex_parser import JavaRegexParser


class JavaFile(Libg3nFile):

    _regex_parser = JavaRegexParser()
    _parsed_functions = None
    _function_matches = []
    _offset = 0

    @property
    def file_extension(self) -> str:
        return 'java'

    def parse(self):
        # Read the file and store the contents in _code
        self.read()
        # Find and parse all decorated functions
        self._parsed_functions = self._regex_parser.parse_file(self.path)

    def process(self, config: Libg3nConfig):
        # Iterate over previously parsed functions
        for function in self._parsed_functions.values():
            # Iterate over functions found in the config
            for config_function in config.functions.values():
                # Try if function idents match
                if config_function.matches(function, self._regex_parser.GroupNames.IDENT):
                    # Touch this file to mark it has been modified and needs to be unparsed
                    self.touch()
                    # Connect the matched function by saving it in the config function
                    config_function.match = function
                    self._function_matches.append(config_function)
                    # self._function_matches[config_function.ident] = {'function': function, 'config': config_function}

    def unparse(self) -> str:
        self._offset = 0

        # Iterate over the matched functions
        for function in self._function_matches:

            # Only continue in case function was loaded with the match token
            if function.matched:
                # Generate the function code segment
                function_code = function.generate_body()

                # Insert the code into the original sourcecode
                self.code = self._insert_between(function_code, function.start_line(), function.end_line())

        return self.code

    def _insert_between(self, payload: str, start: int, end: int) -> str:

        # Preserve original length
        length = len(self.code)

        # Add offset to start and end positions
        start_index = start + self._offset
        end_index = end + self._offset

        print(start_index)
        print(end_index)

        # Insert the payload code
        result = self.code[:start_index] + payload + self.code[end_index:]

        # Compare lengths and add new offset
        self._offset += len(result) - length

        # Return the resulting sourcecode
        return result
