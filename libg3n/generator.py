import os

from strenum import StrEnum
from enum import auto

import libg3n
from libg3n.model.libg3n_library import Libg3nLibrary
from libg3n.model.libg3n_config import Libg3nConfig


class GeneratorConfigKeys(StrEnum):
    OUTPUT_DIR = auto()
    CLASS_SUBFOLDER = auto()
    CLASS_PREFIX = auto()
    SKIP_FUNCTIONS = auto()


class Generator:

    # Singleton instance
    _instance = None

    # Config Values
    _output_directory: str = './generated/'

    _class_subfolder: str = ''

    _class_prefix: str = ''

    _skip_functions: bool = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Generator, cls).__new__(cls)
        return cls._instance

    def generate(self, library: Libg3nLibrary, config: Libg3nConfig):

        libg3n.logger.debug('Initiated library generation from ' + library.path)

        # Perform the library scan
        library.scan()

        libg3n.logger.debug('Found ' + str(library.number_of_files) + ' matching files in the library')

        # In case the functions are not skipped by the configuration
        if not self._skip_functions:

            # Traverse through library files
            for file in library.files:

                libg3n.logger.debug('Processing File: ' + file.path)

                # Parse file to AST
                file.parse()

                file.process(config)

                if file.touched():

                    libg3n.logger.debug('File ' + file.path + ' was altered!')
                    # Unparse the AST back to python code
                    file.unparse()

                    # Write the generated file
                    file.write(file_path=self._output_directory)
        else:
            libg3n.logger.debug('Skipping function generation as specified in the configuration.')

        # Get class output path and create it in case it doesn't exist
        class_output_path = self._output_directory + '/' + self._class_subfolder + '/'

        if not os.path.isdir(class_output_path):
            os.mkdir(class_output_path)

        # Build classes
        for cls in config.classes.values():
            cls.write(class_path=class_output_path, class_prefix=self._class_prefix)

    def set_output_directory(self, path: str):
        """
        Function to manually set the output path. Useful because it's the most variable option which is changed often.
        """
        self._output_directory = path

    def load_config(self, config_dict: dict):
        """
        Loads a Config dictionary to quickly configure the Generator
        """
        if GeneratorConfigKeys.OUTPUT_DIR in config_dict:
            self._output_directory = config_dict[GeneratorConfigKeys.OUTPUT_DIR]

        if GeneratorConfigKeys.CLASS_SUBFOLDER in config_dict:
            self._class_subfolder = config_dict[GeneratorConfigKeys.CLASS_SUBFOLDER]

        if GeneratorConfigKeys.CLASS_PREFIX in config_dict:
            self._class_prefix = config_dict[GeneratorConfigKeys.CLASS_PREFIX]

        if GeneratorConfigKeys.SKIP_FUNCTIONS in config_dict:
            self._skip_functions = config_dict[GeneratorConfigKeys.SKIP_FUNCTIONS]

    def write_file(self, file_name: str, content: str):
        # Write the code back to python file

        libg3n.logger.debug('Writing file to: ' + self._output_directory + file_name)
        with open(self._output_directory + file_name, 'w', encoding='utf-8') as f:
            f.write(content)
