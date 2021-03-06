from abc import abstractmethod

from libg3n.model.libg3n_config_parser import Libg3nConfigParser

from libg3n.model.libg3n_function import FunctionType
from libg3n.model.libg3n_function import Libg3nFunction
from libg3n.model.libg3n_class import Libg3nClass
from libg3n.exception.ConfigSyntaxException import ConfigSyntaxException
from libg3n.exception.InvalidTokenException import InvalidTokenException
from libg3n.exception.FailedTokenizationException import FailedTokenizationexception
from libg3n.exception.EmptyFileException import EmptyFileException


class Libg3nConfigParserG3n(Libg3nConfigParser):
    """
    Abstract class which inherits the Libg3nConfigParser class. This class is designed to parse libg3n configs with the
    .gen syntax.
    """
    # Literals
    FUNCTION_KEYWORD = 'function'
    CLASS_KEYWORD = 'class'
    PROPERTY_KEYWORD = 'property'

    KEYWORDS_LEVEL1 = [FUNCTION_KEYWORD, CLASS_KEYWORD]
    KEYWORDS_LEVEL2 = [PROPERTY_KEYWORD]

    # Symbols
    SYMBOLS = [':']
    NULLWORDS = [' ', '\n', '\t']
    STOPWORDS = SYMBOLS + NULLWORDS

    # String Delimiters
    STRING_DELIMITERS = ['"', '\'']

    # Join Keywords
    KEYWORDS = KEYWORDS_LEVEL1 + KEYWORDS_LEVEL2

    # Config token
    _tokenized_config = None

    # Config token array
    _token_array = []

    # Current processed line
    _current_line = 0

    # Parsed functions
    _functions = {}

    # Parsed classes
    _classes = {}

    def parse(self, path) -> dict:
        """
        Parses the config file and produces a dictionary of Libg3n functions and classes.
        """
        # Read the config file
        self._load_file(path)

        # If config was correctly loaded
        if self._config:

            # Tokenize the config contents
            self._tokenized_config = self.tokenize(self._config)

            # If tokenization was successful
            if self._tokenized_config:

                # Split Token into array
                self._token_array = self.split_token_array(self._tokenized_config)

                # If token array was created
                if self._token_array:

                    # Iterate over all token
                    for token in self._token_array:

                        # Parse the token
                        self.parse_token(token)

                    return {self.FUNCTION_DICT_KEY: self._functions, self.CLASS_DICT_KEY: self._classes}
            else:
                raise FailedTokenizationexception()
        else:
            raise EmptyFileException(path)

    def tokenize(self, content: str) -> list:
        """
        Splits a string into a list of token.
        """

        # Current lex token
        lex = ''

        # Result list
        result = []

        # Determine maximum index so we dont overstep the content bounds
        max_length = len(content) - 2

        # Determine if we currently lexing a String
        in_string = False

        # Iterate over all chars in the config
        for i, char in enumerate(content):

            if i != max_length and char not in self.STOPWORDS:

                # Continue Lexing -----

                # Append char in case it's not a nullword
                if char not in self.NULLWORDS and char not in self.STRING_DELIMITERS:
                    lex += char

                # String Handling -----

                if char in self.STRING_DELIMITERS:
                    if in_string:
                        in_string = False
                        result.append(lex)
                        lex = ''
                        continue
                    else:
                        in_string = True
                        lex = ''
                        continue

                if in_string:
                    continue

                # Keyword Handling -----

                # In case we found a valid keyword with the lex
                if self._is_valid_keyword(lex, content[i + 1]):
                    result.append(lex)
                    lex = ''

            else:

                if lex:
                    result.append(lex)
                    lex = ''

                if char in self.SYMBOLS:
                    result.append(char)

        return result

    def _is_valid_keyword(self, string: str, successor: str) -> bool:
        """
        Returns true in case the given String is a valid keyword.
        """
        return (string in self.KEYWORDS and successor in self.STOPWORDS) or (string in self.SYMBOLS)

    def split_token_array(self, token_array: list) -> list:
        """
        Splits a token list by applying the function and class syntax.
        """

        # Result list
        result = []

        # Current syntax part
        part = []

        # Determine maximum index so we don't overstep array bounds
        length = len(token_array) - 1

        # Iterate over all token
        for i, token in enumerate(token_array):

            # In case the token matches with a level 1 keyword
            if token in self.KEYWORDS_LEVEL1:
                # In case the part has an actual value
                if part:
                    result.append(part)
                    part = []

            # Append the token to the current part
            part.append(token)

            # In case we reach the end, save the last token to the current part
            if i == length:
                result.append(part)

        return result

    def parse_token(self, token: list):
        """
        Parses a single token into a function / class.
        """

        # Determine if the token is a (valid) function / class
        if self.is_function_token(token) and self.validate_function_token(token):
            result = self.process_function(token)
            self._functions[result.ident] = result
        elif self.is_class_token(token) and self.validate_class_token(token):
            result = self.process_class(token)
            self._classes[result.name] = result
        else:
            # TODO: Find error position
            raise InvalidTokenException(token, self._path)

        return result

    def is_function_token(self, token) -> bool:
        """
        Determines if the given token is a function token.
        """
        result = False
        if token[0] == self.FUNCTION_KEYWORD:
            result = True
        return result

    def is_class_token(self, token) -> bool:
        """
        Determines if the given token is a class token.
        """
        result = False
        if token[0] == self.CLASS_KEYWORD:
            result = True
        return result

    def validate_function_token(self, token) -> bool:
        """
        Determines if the given function token is valid.
        """
        valid = True
        if token[0] != self.FUNCTION_KEYWORD or \
                token[2] not in self.SYMBOLS or \
                token[3] not in self.FUNCTION_TYPES.keys():
            valid = False
        return valid

    def validate_class_token(self, token) -> bool:
        """
        Determines if the given class token is valid.
        """
        valid = True
        # TODO: Rework
        if token[0] != self.CLASS_KEYWORD or \
                (token[2] in self.SYMBOLS and token[4] != self.PROPERTY_KEYWORD):
            valid = False
        return valid

    @abstractmethod
    def process_function(self, function_element) -> Libg3nFunction:
        """
        Abstract function which should implemented to map a config function element to a libg3n function.
        """
        pass

    @abstractmethod
    def process_class(self, class_element) -> Libg3nClass:
        """
        Abstract function which should implemented to map a config class element to a libg3n class.
        """
        pass
