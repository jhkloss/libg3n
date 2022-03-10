class InvalidFileException(Exception):

    def __init__(self, path: str, purpose: str = "General"):
        # Path to the file
        self.path = path
        # Optional use of the file, helps the user understand for which purpose the file was used.
        self.purpose = purpose

    def __str__(self):
        return "{purpose} file {path} was does not exist.".format(purpose=self.purpose, path=self.path)
