import libg3n
from abc import ABC, abstractmethod
from enum import IntEnum, unique, auto

# To differ between function types to be generated we have to define them in advance. The place of choice to define
# these is this file because these types are only used in the context of decorators.

# Define the function types as enum. We start at zero so we can use the LENGTH member to get the number of types without
# an additonal function call.


@unique
class FunctionType(IntEnum):
    RETURN = auto()
    CUSTOM = auto()
    EXTERNAL = auto()
    LENGTH = auto()


class Libg3nFunction(ABC):
    _ident: str
    _function_type: FunctionType
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
    def type(self, function_type: FunctionType):
        self._function_type = function_type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: any):
        self._value = value

    def generate_body(self) -> str:
        result = ""
        # Return the matching function body according to the type
        # TODO: Replace with match-case statement, once upgraded to python 3.10
        libg3n.logger.debug('Generating ' + str(self._function_type) + ' function body for ' + str(self._ident))

        if self._function_type == FunctionType.RETURN:
            result = self._return_function_body()
        elif self._function_type == FunctionType.CUSTOM:
            result = self._custom_function_body()
        elif self._function_type == FunctionType.EXTERNAL:
            result = self._external_function_body()

        return result

    @abstractmethod
    def _return_function_body(self) -> any:
        pass

    @abstractmethod
    def _custom_function_body(self) -> any:
        pass

    @abstractmethod
    def _external_function_body(self) -> any:
        pass
