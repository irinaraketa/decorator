class NotCorrectColorIndex(Exception):
    def __init__(self, tect):
        self.txt = tect
        