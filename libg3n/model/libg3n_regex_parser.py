import os.path
from abc import ABC, abstractmethod
from strenum import StrEnum
import re

import libg3n
from libg3n.exception.InvalidFileException import InvalidFileException
from libg3n.exception.InvalidParsingSyntaxException import InvalidParsingSyntaxException


# TODO: Inherit from normal Config parser
class Libg3nRegexParser(ABC):

    class GroupNames(StrEnum):
        NAME = 'name'
        IDENT = 'ident'
        PARAMETER = 'pram'
        MODIFICATOR = 'mod'
        TYPE = 'type'
        SIGNATURE = 'sig'
        LINE_START = 'line_start'
        LINE_END = 'line_end'

    @property
    def regex_spacer(self) -> str:
        return r'\n?(\s*|\t*)'

    @property
    def regex_annotation_symbol(self) -> str:
        return '@'

    @property
    def regex_annotation_name(self) -> str:
        return 'Generate'

    @property
    def regex_annotation_param_name(self) -> str:
        return 'ident'

    @property
    def regex_annotation_param(self) -> str:
        return r'.+'

    @property
    def regex_annotation(self) -> str:
        """
        Prebuilds the annotation regex with use of the predefined parts.
        """
        return self.regex_annotation_symbol + self.regex_annotation_name + '\(' + self.regex_annotation_param_name + self.regex_spacer + '=' \
               + self.regex_spacer + '("|\')' \
               + self._add_regex_group(self.regex_annotation_param, self.GroupNames.IDENT) + '("|\')' \
               + self.regex_spacer + '\)'

    @property
    @abstractmethod
    def regex_modificator(self) -> str:
        pass

    @property
    @abstractmethod
    def regex_type(self) -> str:
        pass

    @property
    @abstractmethod
    def regex_sig(self) -> str:
        pass

    @property
    def regex_body(self) -> str:
        return r'{(.*\n)*}'

    @property
    @abstractmethod
    def regex_string(self) -> str:
        """
        Builds the complete regex string by using the class functions for single regex parts.
        """
        pass

    @staticmethod
    def syntax_check(code: str) -> bool:
        """
        Checks the syntax of the given code. This function defaults to True and needs to be implemented and adjusted to
        the given programming language. It is used in the parsing function of this class, which means it should either
        be properly implemented or should default to True, otherwise the parsing may fail.
        """
        return True

    @staticmethod
    def _add_regex_group(regex: str, group_name: str):
        """
        Adds the group syntax to any regex string. The group name is defined by the group_name parameter.
        """
        return f'(?P<{group_name}>' + regex + ')'

    @staticmethod
    def glue_regex_token_list(token_list: list) -> str:
        result = ''
        length = len(token_list) - 1

        for i, token in enumerate(token_list):
            result += token
            if i < length:
                result += '|'

        return '({result})'.format(result=result)

    def parse_file(self, file_path: str) -> dict:
        """
        Parses a specific file and produces a dict with all annotation matches.
        """

        libg3n.logger.debug('Regex Parsing file: ' + file_path)

        if os.path.exists(file_path):
            with open(file_path) as f:
                content = f.read()
                return self.parse_code(content)
        else:
            raise InvalidFileException()

    def parse_code(self, code: str) -> dict:
        result = {}

        if self.syntax_check(code):
            for match in re.finditer(self.regex_string, code):

                libg3n.logger.debug('Found Regex match in line: ' + str(match.pos))

                # Get regex group_dict for the match
                match_groups = match.groupdict()

                # Add positional metadata to the match
                match_groups[self.GroupNames.LINE_START] = match.start()
                match_groups[self.GroupNames.LINE_END] = match.end()

                # Save the result
                result[match_groups[self.GroupNames.IDENT]] = match_groups

            # Return the result
            return result
        else:
            raise InvalidParsingSyntaxException()
