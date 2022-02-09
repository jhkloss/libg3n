from abc import abstractmethod
import xml.etree.ElementTree as et

import libg3n
from libg3n.model.libg3n_config_parser import Libg3nConfigParser
from libg3n.model.libg3n_function import Libg3nFunction
from libg3n.model.libg3n_class import Libg3nClass


class Libg3nXMLConfigParser(Libg3nConfigParser):

    # Current XML file tree
    _config_tree: et.ElementTree

    # Function XML node name
    CONFIG_FUNCTION_KEYWORD = 'func'

    # Class XML node name
    CONFIG_CLASS_KEYWORD = 'class'

    def parse(self, path: str) -> dict:
        # Load the XML file
        self._load_file(path)

        libg3n.logger.debug('Parsing config file: ' + path)

        # Extract the XML ElementTree
        self.extract_config_tree()

        # Extract functions and classes from the ElementTree
        result = {self.FUNCTION_DICT_KEY: self.get_functions(), self.CLASS_DICT_KEY: self.get_classes()}

        # Return the dict with functions and classes
        return result

    def extract_config_tree(self):
        """
        Extracts an xml.etree.Elementtree from the given xml config file.
        """
        self._config_tree = et.ElementTree(file=self._path)

    def get_functions(self):
        """
        Extracts and returns all functions from the Elementtree representing the xml config file.
        """
        # We use the python hashtable (dict) to quickly access the right functions later
        function_dict = {}

        # Find all function nodes inside the Elementtree
        functions = self._config_tree.findall(self.CONFIG_FUNCTION_KEYWORD)

        libg3n.logger.debug('Found ' + str(len(functions)) + ' functions specified by the config file')

        # Assertion in case we encounter a duplicate function ID
        assert id not in function_dict, 'Encountered duplicate function id!'

        # Iterate over the functions and turn them into Libg3n functions
        for function in functions:
            new_function = self.process_function(function)
            function_dict[new_function.ident] = new_function

        return function_dict

    def get_classes(self):
        """
        Extracts and returns all classes from the Elementtree representing the xml config file.
        """
        # We use the python hashtable (dict) to quickly access the right classes later
        classes_dict = {}

        # Find all class nodes inside the Elementtree
        classes = self._config_tree.findall(self.CONFIG_CLASS_KEYWORD)

        # Iterate over the classes and turn them into Libg3n classes
        for current_class in classes:
            new_class = self.process_class(current_class)
            classes_dict[new_class.name] = new_class

        return classes_dict

    def dump_tree(self):
        """
        Dumps the parsed tree for debugging purposes.
        """
        funcs = self._config_tree.findall(self.CONFIG_FUNCTION_KEYWORD)

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
        """
        Abstract function which should implemented to map a config function element to a libg3n function.
        """
        pass

    @abstractmethod
    def process_class(self, class_element) -> Libg3nClass:
        """
            Abstract function which should implemented to map a config class element to a libg3n class.
        """
        pass
