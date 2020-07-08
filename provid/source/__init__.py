from provid.source._source import Source

from provid.source._national_patient import NationalPatient
from provid.source._county_case import CountyCase
from provid.source._county_death import CountyDeath
from provid.source._county_population import CountyPopulation
from provid.source._princeton import Princeton

def download_all():
    srcs = {}
    for src in [NationalPatient(), CountyCase(), CountyDeath(), CountyPopulation(), Princeton()]:
        print("Downloading {}...".format(src.filename))
        srcs[src.filename] = src
        src.download()

    return srcs
