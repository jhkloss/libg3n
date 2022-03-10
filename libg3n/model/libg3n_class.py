import libg3n

from abc import ABC, abstractmethod
from .libg3n_property import Libg3nProperty


class Libg3nClass(ABC):
    """
    Abstract class describing the Libg3n class template. Implementing classes should implement the to_code function
    regarding the language specification of the representing language module.
    """

    # The class name
    _name: str = ""

    # The name of the metaclass which this class should implement
    _meta_class: str = ""

    # List of class properties
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

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """
        Abstract property. File extension of the file.
        """
        pass

    def add_property(self, property: Libg3nProperty):
        """
        Adds the given property to the properties dict. The property name is used as a dict key.
        """
        self._properties[property.name] = property

    def get_property(self, name: str):
        """
        Returns a property which matches the given property name.
        """
        result = None
        if name in self._properties:
            result = self._properties[name]
        return result

    @abstractmethod
    def to_code(self) -> str:
        """
        Abstract function which turns the class metadata into an actual class specification.
        """
        pass

    def write(self, class_path: str = '', class_name: str = '', class_prefix: str = '', encoding: str = 'utf-8'):
        """
        Writes the class to a file.
        """

        # If there is no class name specified, use the Ident instead
        if not class_name:
            class_name = self._name

        # Construct the resulting path
        result_path = class_path + class_prefix + class_name + '.' + self.file_extension

        libg3n.logger.debug('Writing class: ' + result_path)

        # Generate the class code
        code = self.to_code()

        # Make sure the sourcecode is valid before it is written
        if code:
            # Write the sourcecode to a new file.
            with open(result_path, 'w', encoding=encoding) as f:
                f.write(code)
