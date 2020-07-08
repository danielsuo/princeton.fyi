import pandas as pd

from provid.source._source import Source

class Princeton(Source):
    def __init__(self):
        super().__init__()
        self.url = "https://docs.google.com/spreadsheets/d/1b-nTEu7ND92SQvnM-SVR5MpgdrQhMrwjD_xReDDll3E/export?format=csv"
        self.filename = "princeton"
        self.ext = "csv"

        self.set_path()

    def parse(self):
        with open(self.raw_path, "r") as f:
            self.df = pd.read_csv(f, index_col=0)
