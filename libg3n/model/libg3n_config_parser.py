from abc import ABC, abstractmethod
import xml.etree.ElementTree as et

from libg3n.model.libg3n_function import FunctionType
from libg3n.model.libg3n_function import Libg3nFunction
from libg3n.model.libg3n_class import Libg3nClass


class Libg3nConfigParser(ABC):

    # Current XML file tree
    _config_tree: et.ElementTree

    FUNCTION_TYPES = {
        'Return': FunctionType.RETURN,
        'Value': FunctionType.VALUE,
        'Custom': FunctionType.CUSTOM,
        'External': FunctionType.EXTERNAL,
    }

    # Loads an config xml file and extracts the element tree.
    def load_file(self, path):
        if exists(path):
            self._config_tree = et.ElementTree(file=path)


    def get_functions(self):
        # We use the python hashtable (dict) to quickly access the right functions later
        function_dict = {}
        functions = self._config_tree.findall('func')

        assert id not in function_dict, 'Encountered duplicate function id!'

        for function in functions:
            new_function = self.process_function(function)
            function_dict[new_function.ident] = new_function

        return function_dict

    def get_classes(self):

        classes_dict = {}
        classes = self._config_tree.findall('class')

        for current_class in classes:
            new_class = self.process_class(current_class)
            classes_dict[new_class.name] = new_class

        return classes_dict

    def _parse_function_type(self, function_type_string) -> FunctionType:
        function_type = FunctionType.RETURN

        if function_type_string == 'Return':
            function_type = FunctionType.RETURN
        elif function_type_string == 'Value':
            function_type = FunctionType.VALUE
        elif function_type_string == 'Custom':
            function_type = FunctionType.CUSTOM
        elif function_type_string == 'External':
            function_type = FunctionType.EXTERNAL
        else:
            libg3n.logger.error('Config Parse: Invalid function type was specified')

        return function_type

    # Dumps the parsed tree for debuging purposes.
    def dump_tree(self):

        funcs = self.current_tree.findall('func')

        print(('Functions').center(40, '-'))

        for func in funcs:
            id = func.find('id').text
            type = func.find('type').text
            value = func.find('value').text
            print(('Function ' + id).ljust(40, '-'))
            print('Type: ' + type)
            print('Value: ' + value)

    @abstractmethod
    def process_function(self, function_element) -> Libg3nFunction:
        pass

    @abstractmethod
    def process_class(self, class_element) -> Libg3nClass:
        pass
