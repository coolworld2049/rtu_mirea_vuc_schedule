class WorksheetNotExist(Exception):
    def __init__(self, msg):
        self.message = msg
        super().__init__()


class WorksheetCount(Exception):
    def __init__(self, msg):
        self.message = msg
        super().__init__()
