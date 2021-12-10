class InvalidTokenException(Exception):

    def __init__(self, token: list, path="", line=0):
        self.token = token
        self.path = path
        self.line = line
        super().__init__()

    def __str__(self):

        result = "Encountered invalid token: " + self.token[0]

        if self.path:
            result += " in file: " + self.path

        if self.line:
            result += " in line:" + str(self.line)

        return result
