from provid.source._source import Source

class StateData(Source):
    def __init__(self):
        super().__init__()
        self.url = "https://covidtracking.com/api/v1/states/daily.csv"
        self.filename = "state_data"
        self.ext = "csv"

        self.set_path()
