from provid.source._source import Source

class CountyPopulation(Source):
    def __init__(self):
        super().__init__()
        self.url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv"
        self.filename = "county_population"
        self.ext = "csv"

        self.set_path()
