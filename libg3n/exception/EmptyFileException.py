class EmptyFileException(Exception):

    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return 'File {path} is empty.'.format(path=self.path)