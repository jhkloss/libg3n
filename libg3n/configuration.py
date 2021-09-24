from libg3n.modules.python.python_config_parser import XMLParser


class Configuration:

    __path: str
    __functions = {}
    __classes = {}
    __parser = XMLParser()

    @property
    def functions(self):
        return self.__functions

    @property
    def classes(self):
        return self.__classes

    def __init__(self, path):
        self.__path = path
        self.__parser.load_file(path)
        self.__functions = self.__parser.get_functions()
        self.__classes = self.__parser.get_classes()
