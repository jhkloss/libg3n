from abc import ABC, abstractmethod
from .libg3n_property import Libg3nProperty


class Libg3nClass(ABC):
    _name: str
    _meta_class: str
    _properties = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def meta_class(self):
        return self._meta_class

    @meta_class.setter
    def meta_class(self, meta_class: str):
        self._meta_class = meta_class

    @property
    def properties(self):
        return self._properties

    def add_property(self, property: Libg3nProperty):
        self._properties[property.name] = property

    def get_property(self, name: str):
        result = None
        if name in self._properties:
            result = self._properties[name]
        return result

    def glue_properties(self):
        result = []
        for property in self._properties.values():
            result.append(property.to_ast())
        return result

    @abstractmethod
    def to_ast(self):
        pass

    @abstractmethod
    def to_code(self):
        pass
