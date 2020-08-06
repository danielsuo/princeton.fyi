from provid.source._source import Source

class StateData(Source):
    def __init__(self):
        super().__init__()
        self.url = "https://api.covidtracking.com/v1/states/nj/daily.csv"
        self.filename = "state_data"
        self.ext = "csv"

        self.set_path()
