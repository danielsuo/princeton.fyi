from provid.source._source import Source

class NationalData(Source):
    def __init__(self):
        super().__init__()
        self.url = "https://covidtracking.com/api/v1/us/daily.csv"
        self.filename = "national_data"
        self.ext = "csv"

        self.set_path()
