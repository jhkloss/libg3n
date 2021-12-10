class ConfigSyntaxException(Exception):

    def __init__(self, file, line):
        self.file = file
        self.line = line
        super().__init__()

    def __str__(self):
        return "Encountered an Syntax Error whilst parsing " + self.file + " in line" + str(self.line)
