from abc import abstractmethod
import xml.etree.ElementTree as et

from libg3n.model.libg3n_config_parser import Libg3nConfigParser
from libg3n.model.libg3n_function import Libg3nFunction
from libg3n.model.libg3n_class import Libg3nClass


class Libg3nXMLConfigParser(Libg3nConfigParser):

    # Current XML file tree
    _config_tree: et.ElementTree

    def parse(self, path: str) -> dict:
        # Load the XML file
        self._load_file(path)

        # Extract the XML ElementTree
        self.extract_config_tree()

        # Extract functions and classes from the ElementTree
        result = {self.FUNCTION_DICT_KEY: self.get_functions(), self.CLASS_DICT_KEY: self.get_classes()}

        # Return the dict with functions and classes
        return result

    def extract_config_tree(self):
        self._config_tree = et.ElementTree(file=self._path)

    def get_functions(self):
        # We use the python hashtable (dict) to quickly access the right functions later
        function_dict = {}
        functions = self._config_tree.findall('func')

        # Assertion in case we encounter a duplicate function ID
        assert id not in function_dict, 'Encountered duplicate function id!'

        # Iterate over the functions and turn them into Libg3n functions
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

    # Dumps the parsed tree for debugging purposes.
    def dump_tree(self):

        funcs = self._config_tree.findall('func')

        print('Functions'.center(40, '-'))

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
