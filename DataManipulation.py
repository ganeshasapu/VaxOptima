"""File for data manipulation for data in datasets folder"""
import pandas as pd
import json


VACCINE_HESITANCY_RATE_CONTINENT = {"Asia": 0.15,
                                    "Europe": 0.25,
                                    "North America": 0.25,
                                    "South America": 0.15,
                                    "Oceania": 0.3,
                                    "Africa": 0.4}

# Shipment Time Meaning:
# 1 - Same Continent
# 2 - Same Hemisphere
# 3 - Different Hemisphere
VACCINE_SHIPMENT_TIME_CONTINENT = {"Asia": {"Europe": 2,
                                            "North America": 3,
                                            "South America": 3,
                                            "Oceania": 2,
                                            "Africa": 2,
                                            "Asia": 1},
                                   "Europe": {"Europe": 1,
                                              "North America": 3,
                                              "South America": 3,
                                              "Oceania": 2,
                                              "Africa": 2,
                                              "Asia": 2},
                                   "North America": {"Europe": 3,
                                                     "North America": 1,
                                                     "South America": 2,
                                                     "Oceania": 3,
                                                     "Africa": 3,
                                                     "Asia": 3},
                                   "South America": {"Europe": 3,
                                                     "North America": 2,
                                                     "South America": 1,
                                                     "Oceania": 3,
                                                     "Africa": 3,
                                                     "Asia": 3},
                                   "Oceania": {"Europe": 2,
                                               "North America": 3,
                                               "South America": 3,
                                               "Oceania": 1,
                                               "Africa": 2,
                                               "Asia": 2},
                                   "Africa": {"Europe": 2,
                                              "North America": 3,
                                              "South America": 3,
                                              "Oceania": 2,
                                              "Africa": 1,
                                              "Asia": 2}}

# These exporters make up the vast majority of covid vaccine exports
VACCINE_EXPORTERS = {"Germany": 512484000,
                     "Spain": 268444000,
                     "Belgium": 1488600000,
                     "China": 1986400000,
                     "United States of America": 968000000,
                     "South Korea": 240400000,
                     "India": 140200000,
                     "South Africa": 110100000,
                     "Russia": 102400000,
                     "Japan": 67000000}


def get_export_rate() -> dict[str: int]:
    """Returns a dictionary mapping an exporter to its export rate of vaccine"""
    country_vac_export_rate = {c: (VACCINE_EXPORTERS[c] // 730) for c in VACCINE_EXPORTERS}
    return country_vac_export_rate


def get_country_pop() -> dict[str: int]:
    """Returns a dictionary mapping a country to its population"""
    populations = _create_df("datasets/population_by_country_2020.csv")
    countries = get_all_countries()

    country_to_pop = {}
    for item in populations.iterrows():
        country = item[1]['Country (or dependency)']
        population = item[1]['Population (2020)']
        if country in countries:
            country_to_pop[country] = population
    return country_to_pop


def get_all_countries_shipment_time() -> dict[str: dict[str: int]]:
    """Returns a dictionary mapping a country to its vaccination shipment time"""
    country_to_cont = _get_country_continent()
    country_shipment_time = {c: VACCINE_SHIPMENT_TIME_CONTINENT[country_to_cont[c]] for c in country_to_cont}
    return country_shipment_time


def get_all_countries_vaxhesitancy() -> dict[str: float]:
    """Returns a dictionary mapping a country to its vaccination hesitancy rate. Note that we generalize the vaccine
    hesitancy rate of each continent to each country due to lack of data"""
    country_to_cont = _get_country_continent()
    country_vaxhesitancy = {c: VACCINE_HESITANCY_RATE_CONTINENT[country_to_cont[c]] for c in country_to_cont}
    return country_vaxhesitancy


def get_all_country_vaxrate() -> dict[str: float]:
    """Returns a dictionary mapping a country to its vaccination rate"""
    df = _create_df("datasets/vaccinations.csv")
    countries = get_all_countries()
    country_avg_vax_rate = {c: _get_avg_daily_vax_rate(df, c) for c in countries}
    return country_avg_vax_rate


def get_all_countries() -> set | dict:
    """Get all countries"""
    continent = set(_create_df("datasets/continents-according-to-our-world-in-data.csv")["Entity"].unique())
    vaccine = set(_create_df("datasets/vaccinations.csv")["location"].unique())
    population = set(_create_df("datasets/population_by_country_2020.csv")['Country (or dependency)'].unique())

    # Filtering countries with valid data
    countries_with_data = continent.intersection(vaccine, population)

    countries = []
    with open("datasets/world-countries.json") as file:
        data = json.load(file)
        features = data["features"]
        for f in features:
            countries.append(f["properties"]["name"])

    valid_countries = {c for c in countries if c in countries_with_data}
    return valid_countries


# Helper Methods
def _create_df(file: str) -> pd.DataFrame:
    """Helper method to create data frame given csv file"""
    df = pd.read_csv(file)
    return df


def _get_country_continent() -> dict[str: str]:
    """Helper method to return a dict mapping countries to their continents"""
    countries = get_all_countries()
    continent_df = _create_df("datasets/continents-according-to-our-world-in-data.csv")

    country_vaxhesitacny = {}
    for item in continent_df.iterrows():
        country = item[1]['Entity']
        continent = item[1]['Continent']
        if country in countries:
            country_vaxhesitacny[country] = continent
    return country_vaxhesitacny


def _get_avg_daily_vax_rate(df: pd.DataFrame, country: str) -> float:
    """Helper method average vaccine rate given a country

    Preconditions:
        - dataframe includes column, "daily_vaccinations_per_million"
        - country name is formatted correctly
    """
    df_country = df[df['location'] == country]
    avg_vax_rate = df_country["daily_vaccinations_per_million"].mean() / 1000000
    return avg_vax_rate


# Testing
if __name__ == "__main__":
    x = get_all_country_vaxrate()
    y = get_all_countries_vaxhesitancy()
    z = get_country_pop()
    b = get_export_rate()
    j = get_all_countries_shipment_time()

    print(x)
    print(len(x))
    print(y)
    print(len(y))
    print(z)
    print(len(z))
    print(b)
    print(len(b))
    print(j)
    print(len(j))
