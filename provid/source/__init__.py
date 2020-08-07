import datetime
import pandas as pd
import numpy as np
import simplejson as json

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
        table[col].iloc[: np.argmin(table[col])] = 0

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
        "total_positive": data["princeton"].df.total_positive.iloc[::-1],
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

    local_table["rolling_total_tests"] = local_table.total_tests.rolling(7).mean()
    local_table["rolling_positive_tests"] = local_table.total_positive.rolling(7).mean()
    local_table["positive_test_rate"] = (
        local_table.rolling_positive_tests / local_table.rolling_total_tests * 100
    )

    local_table.to_csv("data/local.csv")
    local_table.new_cases.to_csv("data/local_case.csv")
    local_table[["new_tests", "positive_test_rate"]].to_csv("data/local_test.csv")
    local_table.new_deaths.to_csv("data/local_death.csv")

    return local_table


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
        #     "total_active": data["princeton"].df.active_positive.iloc[::-2].rename("total_active"),
        #     "total_tests": (data["princeton"].df.total_positive.iloc[::-2] + data["princeton"].df.total_negative.iloc[::-2]).rename("total_tests")
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

    county_table.to_csv("data/county.csv")
    county_table.new_cases.to_csv("data/county_case.csv")
    county_table.new_deaths.to_csv("data/county_death.csv")
    county_table["new_tests"] = 0
    county_table["positive_test_rate"] = 0
    county_table[["new_tests", "positive_test_rate"]].to_csv("data/county_test.csv")

    return county_table


def update_state(data, dates):
    state = data["state_data"].df[data["state_data"].df.state == "NJ"]
    state.index = pd.to_datetime(state.date, format="%Y%m%d")

    state_table = pd.merge(
        pd.DataFrame(dates), state, how="outer", left_index=True, right_index=True
    )
    state_table = state_table._get_numeric_data()
    state_table = pad_zeros(state_table)
    state_table = state_table.fillna(method="ffill")
    # state_table = state_table.interpolate(method="time", limit_direction="both")
    state_table["total_tests"] = state_table.positive + state_table.negative
    state_table["total_cases"] = state_table.positive
    state_table["total_deaths"] = state_table.death
    state_table["total_active"] = (
        state_table.positive - state_table.death - state_table.recovered
    )

    state_table["total_positive"] = state_table.positive

    state_table = state_table[
        ["total_tests", "total_cases", "total_deaths", "total_active", "total_positive"]
    ]
    state_diffs = state_table.diff()
    state_diffs.columns = [col.replace("total", "new") for col in state_table.columns]

    state_table = pd.concat([state_table, state_diffs], axis=1)
    state_table = state_table.fillna(value=0)
    state_table[state_table < 0] = 0

    state_table["rolling_total_tests"] = state_table.total_tests.rolling(7).mean()
    state_table["rolling_positive_tests"] = state_table.total_positive.rolling(7).mean()
    state_table["positive_test_rate"] = (
        state_table.rolling_positive_tests / state_table.rolling_total_tests * 100
    )

    state_table.to_csv("data/state.csv")
    state_table.new_cases.to_csv("data/state_case.csv")
    state_table[["new_tests", "positive_test_rate"]].to_csv("data/state_test.csv")
    state_table.new_deaths.to_csv("data/state_death.csv")

    return state_table


def update_national(data, dates):
    national = data["national_data"].df
    national.index = pd.to_datetime(national.date, format="%Y%m%d")

    national_table = pd.merge(
        pd.DataFrame(dates), national, how="outer", left_index=True, right_index=True
    )
    national_table = national_table._get_numeric_data()
    national_table = pad_zeros(national_table)
    national_table = national_table.fillna(method="ffill")
    # national_table = national_table.interpolate(method="time", limit_direction="both")
    national_table["total_tests"] = national_table.positive + national_table.negative
    national_table["total_cases"] = national_table.positive
    national_table["total_deaths"] = national_table.death
    national_table["total_active"] = (
        national_table.positive - national_table.death - national_table.recovered
    )
    national_table["total_positive"] = national_table.positive

    national_table = national_table[
        ["total_tests", "total_cases", "total_deaths", "total_active", "total_positive"]
    ]

    national_diffs = national_table.diff()
    national_diffs.columns = [
        col.replace("total", "new") for col in national_table.columns
    ]

    national_table = pd.concat([national_table, national_diffs], axis=1)
    national_table = national_table.fillna(value=0)
    national_table[national_table < 0] = 0

    national_table["rolling_total_tests"] = national_table.total_tests.rolling(7).mean()
    national_table["rolling_positive_tests"] = national_table.total_positive.rolling(
        7
    ).mean()
    national_table["positive_test_rate"] = (
        national_table.rolling_positive_tests / national_table.rolling_total_tests * 100
    )

    national_table.to_csv("data/national.csv")
    national_table.new_cases.to_csv("data/national_case.csv")
    national_table[["new_tests", "positive_test_rate"]].to_csv("data/national_test.csv")
    national_table.new_deaths.to_csv("data/national_death.csv")

    return national_table


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

    # https://www.census.gov/programs-surveys/popest/data/tables.2019.html
    results = {
        "local": {"population": 31187},
        "state": {"population": 8882190},
        "county": {"population": 367430},
        "national": {"population": 329131338},
    }

    for geo in results:
        table = globals()[f"update_{geo}"](data, dates)

        if "total_active" in table.columns:
            total_active = table.total_active[-2]
            increase_active = np.round(
                (total_active - table.total_active[-9]) / table.total_active[-9] * 100,
                decimals=2,
            )
            per_10k_active = np.round(
                total_active / results[geo]["population"] * 10000, decimals=2
            )

            if np.isnan(increase_active):
                increase_active = 0
        else:
            total_active = "N/A"
            increase_active = "N/A"
            per_10k_active = "N/A"

        new_cases = np.round(
            table.new_cases[-2] / results[geo]["population"] * 10000, decimals=2
        )
        increase_cases = np.round(
            (table.new_cases[-2] - table.new_cases[-9]) / table.new_cases[-9] * 100,
            decimals=2,
        )
        if np.isnan(increase_cases):
            increase_cases = 0

        if "total_tests" in table.columns:
            new_tests = np.round(
                table.new_tests[-2] / results[geo]["population"] * 10000, decimals=2
            )
            increase_tests = np.round(
                (table.new_tests[-2] - table.new_tests[-9]) / table.new_tests[-9] * 100,
                decimals=2,
            )
            if np.isnan(increase_tests):
                increase_tests = 0

            pct_positive = table.positive_test_rate[-2]
            last_pct_positive = table.positive_test_rate[-9]

            increase_pct_positive = np.round(
                (pct_positive - last_pct_positive) / last_pct_positive, decimals=2
            )

            pct_positive = np.round(pct_positive, decimals=2)
            if np.isnan(pct_positive):
                pct_positive = 0
            if np.isnan(increase_pct_positive):
                increase_pct_positive = 0
        else:
            new_tests = "N/A"
            increase_tests = "N/A"
            pct_positive = "N/A"
            increase_pct_positive = "N/A"

        new_deaths = np.round(
            table.new_deaths[-2] / results[geo]["population"] * 10000, decimals=2
        )
        increase_deaths = np.round(
            (table.new_deaths[-2] - table.new_deaths[-9]) / table.new_deaths[-9] * 100,
            decimals=2,
        )

        if np.isnan(increase_deaths):
            increase_deaths = 0

        values = [
            "total_active",
            "per_10k_active",
            "increase_active",
            "new_cases",
            "increase_cases",
            "new_tests",
            "increase_tests",
            "new_deaths",
            "increase_deaths",
            "pct_positive",
            "increase_pct_positive",
        ]

        for value in values:
            results[geo][value] = locals()[value]

        json.dump(results, open("data/cards.json", "w"), ignore_nan=True)


