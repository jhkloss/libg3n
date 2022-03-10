from libg3n.model.libg3n_library import Libg3nLibrary


class EmptyLibraryException(Exception):

    def __init__(self, library: Libg3nLibrary):
        self.library_path = library.path
        self.file_extension = library.file_extension
        super().__init__()

    def __str__(self):
        return "Library {library} contained no files with the Extension .{file_extension}" \
            .format(library=self.library_path, file_extension=self.file_extension)
