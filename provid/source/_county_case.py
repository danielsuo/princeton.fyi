from provid.source._source import Source

class CountyCase(Source):
    def __init__(self):
        super().__init__()
        self.url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv"
        self.filename = "county_case"
        self.ext = "csv"

        self.set_path()
