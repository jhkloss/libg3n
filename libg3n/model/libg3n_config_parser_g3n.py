from abc import ABC, abstractmethod
from os.path import exists

from libg3n.model.libg3n_config_parser import Libg3nConfigParser

from libg3n.model.libg3n_function import FunctionType
from libg3n.model.libg3n_function import Libg3nFunction
from libg3n.model.libg3n_class import Libg3nClass
from libg3n.exception.ConfigSyntaxException import ConfigSyntaxException
from libg3n.exception.InvalidTokenException import InvalidTokenException


class Libg3nConfigParserG3n(Libg3nConfigParser):

    # Literals
    FUNCTION_KEYWORD = 'function'
    CLASS_KEYWORD = 'class'
    PROPERTY_KEYWORD = 'property'

    KEYWORDS_LEVEL1 = [FUNCTION_KEYWORD, CLASS_KEYWORD]
    KEYWORDS_LEVEL2 = [PROPERTY_KEYWORD]
    SYMBOLS = [':']

    NULLWORDS = [' ', '\n']
    STOPWORDS = SYMBOLS + NULLWORDS
    KEYWORDS = KEYWORDS_LEVEL1 + KEYWORDS_LEVEL2 + SYMBOLS

    _tokenized_config = None
    _token_array = []
    _current_line = 0
    _functions = {}
    _classes = {}

    def parse(self, path) -> dict:
        self._load_file(path)

        if self._config:
            self._tokenized_config = self.tokenize(self._config)

            if self._tokenized_config:
                self._token_array = self.split_token_array(self._tokenized_config)

                if self._token_array:

                    for token in self._token_array:
                        self.parse_token(token)

                    return {self.FUNCTION_DICT_KEY: self._functions, self.CLASS_DICT_KEY: self._classes}

            else:
                #TODO: Define Custom Exception
                raise Exception
        else:
            # TODO: Define Custom Exception
            raise Exception

    def tokenize(self, content: str) -> list:
        lex = ''
        result = []
        max_length = len(content) - 1

        for i, char in enumerate(content):

            if lex in self.KEYWORDS:
                result.append(lex)
                lex = ''

            if char not in self.NULLWORDS:
                lex += char

            if i == max_length or content[i + 1] in self.STOPWORDS:
                if lex:
                    result.append(lex)
                    lex = ''

        return result

    def split_token_array(self, token_array: list) -> list:

        result = []
        part = []
        length = len(token_array) - 1

        for i, token in enumerate(token_array):

            if token in self.KEYWORDS_LEVEL1:
                if part:
                    result.append(part)
                    part = []

            part.append(token)

            if i == length:
                result.append(part)

        return result

    def parse_token(self, token: list):

        result = None

        if self.is_function_token(token) and self.validate_function_token(token):
            result = self.process_function(token)
            self._functions[result.ident] = result
        elif self.is_class_token(token) and self.validate_class_token(token):
            result = self.process_class(token)
            self._classes[result.name] = result
        else:
            # TODO: Line herausfinden
            raise InvalidTokenException(token, self._path)

        return result

    def is_function_token(self, token) -> bool:
        result = False
        if token[0] == self.FUNCTION_KEYWORD:
            result = True
        return result

    def is_class_token(self, token) -> bool:
        result = False
        if token[0] == self.CLASS_KEYWORD:
            result = True
        return result

    def validate_function_token(self, token) -> bool:
        valid = True
        if token[0] != self.FUNCTION_KEYWORD or \
           token[2] not in self.SYMBOLS or \
           token[3] not in self.FUNCTION_TYPES.keys():
            valid = False
        return valid

    def validate_class_token(self, token) -> bool:
        valid = True

        # TODO: Rework
        if token[0] != self.CLASS_KEYWORD or \
           (token[2] in self.SYMBOLS and token[4] != self.PROPERTY_KEYWORD):
            valid = False

        return valid

    @abstractmethod
    def process_function(self, function_element) -> Libg3nFunction:
        pass

    @abstractmethod
    def process_class(self, class_element) -> Libg3nClass:
        pass
