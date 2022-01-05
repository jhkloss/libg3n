from abc import ABC, abstractmethod


class Libg3nProperty(ABC):
    _name: str
    _value: any

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: any):
        self._value = value
