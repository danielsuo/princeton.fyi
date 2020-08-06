import datetime
import pandas as pd
import numpy as np

from provid.source._source import Source

from provid.source._national_patient import NationalPatient
from provid.source._national_data import NationalData
from provid.source._state_data import StateData
from provid.source._county_case import CountyCase
from provid.source._county_death import CountyDeath
from provid.source._county_population import CountyPopulation
from provid.source._princeton import Princeton


def download(national_patient=False, fetch=True):
    data = {}
    sources = [
        NationalData(),
        StateData(),
        CountyCase(),
        CountyDeath(),
        CountyPopulation(),
        Princeton(),
    ]

    if national_patient:
        sources.append(NationalPatient())
    for source in sources:
        data[source.filename] = source
        if fetch:
            print("Downloading {}...".format(source.filename))
            source.download()

    return data


def pad_zeros(table):
    for col in table.columns:
        table[col].iloc[:np.argmin(table[col])] = 0

    return table


def update_local(data, dates):
    local = {
        "total_deaths": data["princeton"]
        .df.total_deaths.iloc[::-1]
        .rename("total_deaths"),
        "total_cases": data["princeton"]
        .df.total_positive.iloc[::-1]
        .rename("total_cases"),
        "total_active": data["princeton"]
        .df.active_positive.iloc[::-1]
        .rename("total_active"),
        "total_tests": (
            data["princeton"].df.total_positive.iloc[::-1]
            + data["princeton"].df.total_negative.iloc[::-1]
        ).rename("total_tests"),
    }

    local_table = dates

    for df in local:
        local_table = pd.merge(
            pd.DataFrame(local_table),
            local[df],
            how="outer",
            left_index=True,
            right_index=True,
        )

    local_table = pad_zeros(local_table)

    # local_table = local_table.interpolate(method="time", limit_direction="both")
    local_table = local_table.fillna(method="ffill")
    del local_table[0]

    local_diffs = local_table.diff()
    local_diffs.columns = [col.replace("total", "new") for col in local_table.columns]

    local_table = pd.concat([local_table, local_diffs], axis=1)
    local_table = local_table.round()
    local_table = local_table.fillna(value=0)
    local_table[local_table < 0] = 0

    local_table.to_csv("timeseries/local.csv")
    local_table.new_cases.to_csv("timeseries/local_case.csv")


def update_county(data, dates):
    county = {
        "total_deaths": data["county_death"]
        .df[data["county_death"].df.countyFIPS == 34021]
        .drop(columns=["countyFIPS", "County Name", "State", "stateFIPS"])
        .T.iloc[:, 0]
        .rename("total_deaths"),
        "total_cases": data["county_case"]
        .df[data["county_case"].df.countyFIPS == 34021]
        .drop(columns=["countyFIPS", "County Name", "State", "stateFIPS"])
        .T.iloc[:, 0]
        .rename("total_cases"),
        #     "total_active": data["princeton"].df.active_positive.iloc[::-1].rename("total_active"),
        #     "total_tests": (data["princeton"].df.total_positive.iloc[::-1] + data["princeton"].df.total_negative.iloc[::-1]).rename("total_tests")
    }

    county_table = dates

    for df in county:
        county_table = pd.merge(
            pd.DataFrame(county_table),
            county[df],
            how="outer",
            left_index=True,
            right_index=True,
        )

    county_table = pad_zeros(county_table)
    # county_table = county_table.interpolate(method="time", limit_direction="both")

    county_table = county_table.fillna(method="ffill")
    del county_table[0]

    county_diffs = county_table.diff()
    county_diffs.columns = [col.replace("total", "new") for col in county_table.columns]

    county_table = pd.concat([county_table, county_diffs], axis=1)
    county_table = county_table.fillna(value=0)
    county_table[county_table < 0] = 0

    county_table.to_csv("timeseries/county.csv")


def update_state(data, dates):
    state = data["state_data"].df[data["state_data"].df.state == "NJ"]
    state.index = pd.to_datetime(state.date, format="%Y%m%d")

    state_table = pd.merge(
        pd.DataFrame(dates), state, how="outer", left_index=True, right_index=True
    )
    state_table = state_table._get_numeric_data()
    state_table = pad_zeros(state_table)
    # state_table = state_table.interpolate(method="time", limit_direction="both")
    state_table = state_table.fillna(method="ffill")
    state_table.to_csv("timeseries/state.csv")


def update_national(data, dates):
    national = data["national_data"].df
    national.index = pd.to_datetime(national.date, format="%Y%m%d")

    national_table = pd.merge(
        pd.DataFrame(dates), national, how="outer", left_index=True, right_index=True
    )
    national_table = national_table._get_numeric_data()
    national_table = pad_zeros(national_table)
    # national_table = national_table.interpolate(method="time", limit_direction="both")
    national_table = national_table.fillna(method="ffill")
    national_table.to_csv("timeseries/national.csv")


def update(national_patient=False):
    data = download(national_patient=national_patient, fetch=False)

    for source in data.values():
        source.parse()

    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()

    dates = pd.DataFrame(
        pd.to_datetime(
            [
                start_date + datetime.timedelta(days=delta)
                for delta in range((end_date - start_date).days + 1)
            ]
        )
    )
    dates.index = dates.iloc[:, 0]

    update_local(data, dates)
    update_county(data, dates)
    update_state(data, dates)
    update_national(data, dates)
