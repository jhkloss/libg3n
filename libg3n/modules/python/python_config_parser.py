from libg3n.model.libg3n_config_parser_g3n import Libg3nConfigParserG3n
from libg3n.model.libg3n_function import Libg3nFunction
from libg3n.model.libg3n_class import Libg3nClass
from libg3n.modules.python.python_function import PythonFunction
from libg3n.modules.python.python_property import PythonProperty
from libg3n.modules.python.python_class import PythonClass


class PythonConfigParser(Libg3nConfigParserG3n):

    PROPERTY_TYPE_CONSTANTS = {
        'str': '',
        'int': 0,
        'float': 0.0,
        'bool': True,
    }

    def process_function(self, function_element) -> Libg3nFunction:
        id = function_element[1]
        type = function_element[3]
        value = function_element[4]

        function_type = self._parse_function_type(type)

        return PythonFunction(id, function_type, value)

    def process_class(self, class_element) -> Libg3nClass:

        new_class = PythonClass()

        new_class.name = class_element[1]

        if class_element[2] in self.SYMBOLS:
            new_class.meta_class = class_element[3]

        for i, token in enumerate(class_element):
            if token == self.PROPERTY_KEYWORD:
                new_property = PythonProperty()
                new_property.name = class_element[i + 1]
                new_property.type = class_element[i + 3]
                new_property.value = self.PROPERTY_TYPE_CONSTANTS[new_property.type]
                new_class.add_property(new_property)

        return new_class
