import libg3n
from libg3n.model.libg3n_library import Libg3nLibrary
from libg3n.model.libg3n_config import Libg3nConfig


# Singleton
class Generator:

    _output_directory: str = "./generated/"

    def generate(self, library: Libg3nLibrary, config: Libg3nConfig):

        libg3n.logger.debug('Initiated library generation from ' + library.path)

        # Perform the library scan
        library.scan()

        libg3n.logger.debug('Found ' + str(library.number_of_files) + ' matching files in the library')

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

                # TODO: Copy all other files -> could also be a frontend function

        # Build classes
        for current_class in config.classes.values():
            code = current_class.to_code()

            # TODO: CHECK
            if code:
                libg3n.logger.debug('Unparse class to: ' + self._output_directory + 'class_' + current_class.name)
                self.write_file('class_' + current_class.name + '.py', code)

    def write_file(self, file_name: str, content: str):
        # Write the code back to python file

        libg3n.logger.debug('Writing file to: ' + self._output_directory + file_name)
        with open(self._output_directory + file_name, 'w', encoding='utf-8') as f:
            f.write(content)
