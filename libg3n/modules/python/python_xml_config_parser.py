from libg3n.model.libg3n_config_parser_xml import Libg3nXMLConfigParser
from libg3n.model.libg3n_function import Libg3nFunction
from libg3n.model.libg3n_class import Libg3nClass
from libg3n.modules.python.python_function import PythonFunction
from libg3n.modules.python.python_property import PythonProperty
from libg3n.modules.python.python_class import PythonClass


class PythonXMLConfigParser(Libg3nXMLConfigParser):

    PROPERTY_TYPE_CONSTANTS = {
        'str': '',
        'int': 0,
        'float': 0.0,
        'bool': True,
    }

    def process_function(self, function_element) -> Libg3nFunction:
        id = function_element.find('id').text
        type = function_element.find('type').text
        value = function_element.find('value').text

        function_type = self._parse_function_type(type)

        return PythonFunction(id, function_type, value)

    def process_class(self, class_element) -> Libg3nClass:

        new_class = PythonClass()

        new_class.name = class_element.find('name').text
        new_class.meta_class = class_element.find('metaclass').text

        properties = class_element.findall('property')

        for current_property in properties:
            new_property = PythonProperty()
            new_property.name = current_property.find('name').text
            new_property.value = self.PROPERTY_TYPE_CONSTANTS[current_property.find('type').text]
            new_class.add_property(new_property)

        return new_class
