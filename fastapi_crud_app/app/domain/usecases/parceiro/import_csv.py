from abc import ABC

class AbstractImportCSV:

    def __init__(self, file: str):
        self.file = file

    def upload_csv(self):
        pass
