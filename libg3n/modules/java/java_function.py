import os.path

from libg3n.model.libg3n_function import Libg3nFunction
from libg3n.model.libg3n_regex_parser import Libg3nRegexParser
from libg3n.exception.InvalidFileException import InvalidFileException
from libg3n.exception.EmptyFileException import EmptyFileException


class JavaFunction(Libg3nFunction):

    _match: dict = {}
    _matched: bool = False

    FUNCTION_TEMPLATE = '{mod} {type} {sig} {{\n {code} \n}}'

    def start_line(self) -> int:
        if self._matched:
            return self._match[Libg3nRegexParser.GroupNames.LINE_START]

    def end_line(self) -> int:
        if self._matched:
            return self._match[Libg3nRegexParser.GroupNames.LINE_END]

    @property
    def match(self) -> dict:
        return self._match

    @match.setter
    def match(self, match: dict):
        # Save the match
        self._match = match

        # Mark this function as matched
        self._matched = True

    @property
    def matched(self):
        return self._matched

    def matches(self, match: dict, ident_key: str = 'ident') -> bool:
        return match[ident_key] == self.ident

    def _prepare_value(self):
        if self.match[Libg3nRegexParser.GroupNames.TYPE] == 'String':
            return '"{value}"'.format(value=self.value)
        elif self.match[Libg3nRegexParser.GroupNames.TYPE] == 'boolean':
            if self.value:
                return 'true'
            else:
                return 'false'
        else:
            return self.value

    def _prepare_function_statement(self, code: str) -> str:
        return self.FUNCTION_TEMPLATE.format(mod=self._match[Libg3nRegexParser.GroupNames.MODIFICATOR],
                                             type=self._match[Libg3nRegexParser.GroupNames.TYPE],
                                             sig=self._match[Libg3nRegexParser.GroupNames.SIGNATURE],
                                             code=code)

    def _return_function_body(self) -> any:
        # Prepare value using the _prepare_value function and the return template
        code = 'return {value};'.format(value=self._prepare_value())
        # Return the function code
        return self._prepare_function_statement(code)

    def _custom_function_body(self) -> any:
        return self._prepare_function_statement(self.value)

    def _external_function_body(self) -> any:
        # Check if file exists
        if os.path.exists(self.value):
            # Open file and read content
            with open(self.value) as f:
                code = f.read()
                # Only continue in case we were able to receive the sourcecode
                if code:
                    # Return the prepared statement with injected sourcecode
                    return self._prepare_function_statement(code)
                else:
                    raise EmptyFileException
        else:
            raise InvalidFileException
