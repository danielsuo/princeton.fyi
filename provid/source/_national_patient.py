from provid.source._source import Source

class NationalPatient(Source):
    def __init__(self):
        super().__init__()
        self.url = "https://data.cdc.gov/api/views/vbim-akqf/rows.csv"
        self.filename = "national_patient"
        self.ext = "csv"

        self.set_path()
