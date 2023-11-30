class WorksheetNotExistException(Exception):
    def __init__(self, msg):
        self.message = msg
        super().__init__()


class WorksheetCountException(Exception):
    def __init__(self, msg):
        self.message = msg
        super().__init__()
