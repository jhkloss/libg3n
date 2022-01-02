import libg3n
from libg3n.model.libg3n_class import Libg3nClass
from libg3n.model.libg3n_config_parser import Libg3nConfigParser
from libg3n.model.libg3n_function import Libg3nFunction
from libg3n.modules.java.java_function import JavaFunction
from libg3n.modules.java.java_class import JavaClass
from libg3n.modules.java.java_property import JavaProperty


class JavaConfigParser(Libg3nConfigParser):

    PROPERTY_TYPE_CONSTANTS = {
        'String': '',
        'char': '',
        'int': 0,
        'short': 0,
        'long': 0,
        'byte': 0,
        'float': 0.0,
        'double': 0.0,
        'boolean': True,
        'void': None
    }

    def process_function(self, function_element) -> Libg3nFunction:
        libg3n.logger.debug('Parse Java function from token: ' + function_element)

        id = function_element[1]
        type = function_element[3]
        value = function_element[4]

        function_type = self._parse_function_type(type)

        return JavaFunction(id, function_type, value)

    def process_class(self, class_element) -> Libg3nClass:
        libg3n.logger.debug('Parse Java class from token: ' + class_element)

        new_class = JavaClass()

        new_class.name = class_element[1]

        if class_element[2] in self.SYMBOLS:
            new_class.meta_class = class_element[3]

        for i, token in enumerate(class_element):
            if token == self.PROPERTY_KEYWORD:
                new_property = JavaProperty()
                new_property.name = token[i + 1]
                new_property.type = token[i + 3]
                new_property.value = self.PROPERTY_TYPE_CONSTANTS[new_property.type]
                new_class.add_property(new_property)

        return new_class
