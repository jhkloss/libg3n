import libg3n
from abc import ABC, abstractmethod
from enum import IntEnum, unique, auto

# To differ between function types to be generated we have to define them in advance. The place of choice to define
# these is this file because these types are only used in the context of decorators.

# Define the function types as enum. We start at zero so we can use the LENGTH member to get the number of types without
# an additonal function call.


@unique
class FunctionType(IntEnum):
    """
    Enum representing all valid function types.
    """
    RETURN = auto()
    CUSTOM = auto()
    EXTERNAL = auto()
    LENGTH = auto()


class Libg3nFunction(ABC):
    """
    Abstract Class representing a parsed libg3n function.
    """

    # Ident used for matching this function
    _ident: str

    # Function type
    _function_type: FunctionType

    # Function value / path
    _value: any

    def __init__(self, ident: str, function_type: FunctionType, value: any):
        self._ident = ident
        self._function_type = function_type
        self._value = value

    @property
    def ident(self):
        return self._ident

    @ident.setter
    def ident(self, id: str):
        self._ident = id

    @property
    def function_type(self):
        return self._function_type

    @function_type.setter
    def function_type(self, function_type: FunctionType):
        self._function_type = function_type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: any):
        self._value = value

    def generate_body(self) -> str:
        """
        Generates the function body for this function using the metadata stored inside the class variables.
        """
        result = ""

        libg3n.logger.debug('Generating ' + str(self._function_type) + ' function body for ' + str(self._ident))

        # Return the matching function body according to the type
        # TODO: Replace with match-case statement, once upgraded to python 3.10
        if self._function_type == FunctionType.RETURN:
            result = self._return_function_body()
        elif self._function_type == FunctionType.CUSTOM:
            result = self._custom_function_body()
        elif self._function_type == FunctionType.EXTERNAL:
            result = self._external_function_body()

        return result

    @abstractmethod
    def _return_function_body(self) -> any:
        """
        Generates and returns a return function body.
        """
        pass

    @abstractmethod
    def _custom_function_body(self) -> any:
        """
        Generates and returns a custom function body.
        """
        pass

    @abstractmethod
    def _external_function_body(self) -> any:
        """
            Generates and returns an external defined function body.
        """
        pass
