from provid.source._source import Source

from provid.source._national_patient import NationalPatient
from provid.source._national_data import NationalData
from provid.source._state_data import StateData
from provid.source._county_case import CountyCase
from provid.source._county_death import CountyDeath
from provid.source._county_population import CountyPopulation
from provid.source._princeton import Princeton

def download_all(national_patient=False):
    data = {}
    sources = [NationalData(), StateData(), CountyCase(), CountyDeath(), CountyPopulation(), Princeton()]

    if national_patient:
        sources.append(NationalPatient())
    for source in sources:
        print("Downloading {}...".format(source.filename))
        data[source.filename] = source
        source.download()

    return data
