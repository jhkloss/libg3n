import os
import shutil

from strenum import StrEnum
from enum import auto
from distutils.dir_util import copy_tree

import libg3n
from libg3n.model.libg3n_library import Libg3nLibrary
from libg3n.model.libg3n_config import Libg3nConfig
from libg3n.exception.EmptyLibraryException import EmptyLibraryException


class GeneratorConfigKeys(StrEnum):
    """
    Defines the keys for a configuration dictionary.
    """

    OUTPUT_DIR = auto()         # Root Output dictionary
    CLASS_SUBFOLDER = auto()    # Optional subfolder for generated classes
    CLASS_PREFIX = auto()       # Optional prefix for generated classes
    SKIP_FUNCTIONS = auto()     # Skip functions in case only classes are generated
    COPY_LIBRARY_FILES = auto() # Copy all unmodified library files


class Generator:
    """
    Generator class which encapsulates the Libg3n generation logic. By using a Dict in combination with
    the GeneratorConfigKey Enum a custom configuration can be passed with the function load_config().
    """

    # Singleton instance
    _instance = None

    # Config Values
    _output_directory: str = './generated/'

    # Optional class subfolder
    _class_subfolder: str = ''

    # Optional class prefix
    _class_prefix: str = ''

    # Skip function generation
    _skip_functions: bool = False

    # Copy all unmodified library files
    _copy_library_files: bool = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Generator, cls).__new__(cls)
        return cls._instance

    def generate(self, library: Libg3nLibrary, config: Libg3nConfig):
        """
        Generates the variable library files by using a Library and a Config Object.
        """
        libg3n.logger.debug('Initiated library generation from ' + library.path)

        # Copy library
        if self._copy_library_files:
            copy_tree(library.path, self._output_directory)

        # Perform the library scan
        library.scan()

        libg3n.logger.debug('Found ' + str(library.number_of_files) + ' matching files in the library')

        # Continue in case we found matching files in the library
        if library.number_of_files > 0:

            # In case the functions are not skipped by the configuration
            if not self._skip_functions:

                # Traverse through library files
                for file in library.files:

                    libg3n.logger.debug('Processing File: ' + file.path)

                    # Parse file to AST
                    file.parse()

                    file.process(config)

                    # Only continue in case file was altered and needs to be written
                    if file.touched():
                        libg3n.logger.debug('File ' + file.path + ' was altered!')

                        # Unparse the AST back to python code
                        file.unparse()

                        # Write the generated file
                        file.write(file_path=self._output_directory)

            else:
                libg3n.logger.debug('Skipping function generation as specified in the configuration.')
        else:
            raise EmptyLibraryException(library)

        # Get class output path and create it in case it doesn't exist
        class_output_path = self._output_directory + '/' + self._class_subfolder + '/'

        # Check if class path (including optional subfolders) exist, create a dir otherwise
        if not os.path.isdir(class_output_path):
            os.mkdir(class_output_path)

        # Iterate over classes
        for cls in config.classes.values():
            # Write class to file
            cls.write(class_path=class_output_path, class_prefix=self._class_prefix)

    def set_output_directory(self, path: str):
        """
        Function to manually set the output path. Useful because it's the most variable option which is changed often.
        """
        self._output_directory = path

    def load_config(self, config_dict: dict):
        """
        Loads a Config dictionary to quickly configure the Generator.
        """
        if GeneratorConfigKeys.OUTPUT_DIR in config_dict:
            self._output_directory = config_dict[GeneratorConfigKeys.OUTPUT_DIR]

        if GeneratorConfigKeys.CLASS_SUBFOLDER in config_dict:
            self._class_subfolder = config_dict[GeneratorConfigKeys.CLASS_SUBFOLDER]

        if GeneratorConfigKeys.CLASS_PREFIX in config_dict:
            self._class_prefix = config_dict[GeneratorConfigKeys.CLASS_PREFIX]

        if GeneratorConfigKeys.SKIP_FUNCTIONS in config_dict:
            self._skip_functions = config_dict[GeneratorConfigKeys.SKIP_FUNCTIONS]

        if GeneratorConfigKeys.COPY_LIBRARY_FILES in config_dict:
            self._copy_library_files = config_dict[GeneratorConfigKeys.COPY_LIBRARY_FILES]

    def write_file(self, file_name: str, content: str):
        """
        Writes the contents back to a file.
        """

        libg3n.logger.debug('Writing file to: ' + self._output_directory + file_name)
        with open(self._output_directory + file_name, 'w', encoding='utf-8') as f:
            f.write(content)
