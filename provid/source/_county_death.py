from provid.source._source import Source

class CountyDeath(Source):
    def __init__(self):
        super().__init__()
        self.url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv"
        self.filename = "county_death"
        self.ext = "csv"

        self.set_path()
