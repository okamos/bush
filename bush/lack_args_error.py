class LackArgsError(Exception):
    def __init__(self):
        self.message = "Lack of command name or sub command name"
