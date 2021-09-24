import os

import libg3n
from libg3n.model.libg3n_file import Libg3nFile
from libg3n.model.libg3n_library import Libg3nLibrary
from libg3n.modules.python.python_function_visitor import PythonFunctionVisitor
from libg3n.modules.python.python_library import Library
from .configuration import Configuration


# Singleton
class Generator:

    _output_directory: str = "./generated/"

    def generate(self, library: Libg3nLibrary, config: Configuration):

        libg3n.logger.debug('Initiated library generation from ' + library.path)

        # Perform the library scan
        library.scan()

        libg3n.logger.debug('Found ' + str(library.number_of_files) + ' python files in the library')

        # Traverse through library files
        for file in library.files:

            libg3n.logger.debug('Processing File: ' + file.path)

            # Parse file to AST
            file.parse()

            file.process(config)

            if file.touched():
                # Unparse the AST back to python code
                file.unparse()

                # Write the generated file
                file.write(file_path=self._output_directory)

        # Build classes
        for current_class in config.classes.values():
            code = current_class.to_code()
            libg3n.logger.debug('Unparse class to: ' + self.__output_directory + 'class_' + current_class.name)
            self.write_file('class_' + current_class.name + '.py', code)

    def write_file(self, file_name: str, content: str):
        # Write the code back to python file
        with open(self.__output_directory + file_name, 'w', encoding='utf-8') as f:
            f.write(content)