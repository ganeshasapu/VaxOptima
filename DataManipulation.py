"""File for data manipulation for data in datasets folder"""
import pandas as pd
import json

# Dictionary maps source to destinations and the time it takes to ship to each destination
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

# These exporters make up the vast majority of covid vaccine exports. It maps the exporter to the total amount of doses
# they have produced since vaccine production started.
VACCINE_EXPORTERS = {"Germany": 512484000,
                     "Spain": 268444000,
                     "Belgium": 1488600000,
                     "China": 1986400000,
                     "United States": 968000000,
                     "South Korea": 240400000,
                     "India": 140200000,
                     "South Africa": 110100000,
                     "Russia": 102400000,
                     "Japan": 67000000}


def get_all_country_attributes() -> dict:
    """Function that returns all the attributes of each country in a dictionary"""
    # Getting all countries and initiating data frames
    continent_df = pd.read_csv("datasets\\continents-according-to-our-world-in-data.csv")
    vaccine_df = pd.read_csv("datasets\\vaccinations.csv")
    population_df = pd.read_csv("datasets\\population_by_country_2020.csv")
    countries_on_map = _get_countries_on_map()

    all_country_attributes = {}
    countries = _get_all_countries(continent_df, vaccine_df, population_df, countries_on_map)

    # Continents
    all_country_attributes['Continents'] = countries

    # Vaccine Rate
    vaccine_rates = _get_vaxrates(countries, vaccine_df)
    all_country_attributes["Vaccine Rates"] = vaccine_rates

    # Population
    population = _get_populations(countries, population_df)
    all_country_attributes["Populations"] = population

    # Export Rate
    export_rates = _get_export_rates()
    all_country_attributes["Export Rate"] = export_rates

    # Shipment Time
    shipment_times = _get_shipment_times(countries)
    all_country_attributes["Shipment Times"] = shipment_times

    return all_country_attributes


# ----------------------------------------------------------------------------------------------------------------------
# Helper Methods
# ----------------------------------------------------------------------------------------------------------------------
def _get_all_countries(continent_df: pd.DataFrame,
                       vaccine_df: pd.DataFrame,
                       population_df: pd.DataFrame,
                       countries_on_map: set) -> dict:
    """Helper Method that returns a dict mapping all countries with valid data to its continent"""
    continents = set(continent_df["Entity"].unique())
    vaccines = set(vaccine_df["location"].unique())
    populations = set(population_df['Country (or dependency)'].unique())
    valid_countries = countries_on_map.intersection(continents, vaccines, populations)

    countries_to_continents = {}

    # Mapping country to continent
    for item in continent_df.iterrows():
        country = item[1]['Entity']
        continent = item[1]['Continent']
        if country in valid_countries:
            countries_to_continents[country] = continent

    return countries_to_continents


def _get_vaxrates(countries: dict, vaccines_df: pd.DataFrame) -> dict:
    """Helper Method that returns a dict mapping a country to its vaccination rate"""
    country_avg_vax_rate = {c: _get_avg_daily_vax_rate(vaccines_df, c) for c in countries}
    return country_avg_vax_rate


def _get_populations(countries: dict, population_df: pd.DataFrame) -> dict:
    """Helper Method that returns a dict mapping an exporting country to its export rate"""
    country_to_pop = {}
    for item in population_df.iterrows():
        country = item[1]['Country (or dependency)']
        population = item[1]['Population (2020)']
        if country in countries:
            country_to_pop[country] = population
    return country_to_pop


def _get_export_rates() -> dict:
    """Helper Method that returns a dict mapping a country to its population"""
    country_vac_export_rate = {c: (VACCINE_EXPORTERS[c] // 730) for c in VACCINE_EXPORTERS}
    return country_vac_export_rate

def get_all_country_vaxrate() -> dict[str: float]:
    """Returns a dictionary mapping a country to its vaccination rate"""
    df = _create_df("datasets/vaccinations.csv")
    countries = get_all_countries()
    country_avg_vax_rate = {c: _get_avg_daily_vax_rate(df, c) for c in countries}
    return country_avg_vax_rate

def _get_shipment_times(countries: dict) -> dict:
    """Helper Method that returns a dict mapping an exporter to its shipment time to different continents"""
    shipment_time = {c: VACCINE_SHIPMENT_TIME_CONTINENT[countries[c]] for c in VACCINE_EXPORTERS}
    return shipment_time

def get_all_countries() -> set | dict:
    """Get all countries"""
    continent = set(_create_df("datasets/continents-according-to-our-world-in-data.csv")["Entity"].unique())
    vaccine = set(_create_df("datasets/vaccinations.csv")["location"].unique())
    population = set(_create_df("datasets/population_by_country_2020.csv")['Country (or dependency)'].unique())

def _get_countries_on_map() -> set:
    """Helper Method that returns a set of countries that are represented on the folium map"""
    countries = set()

    countries = []
    with open("datasets/world-countries.json") as file:
        data = json.load(file)
        features = data["features"]
        for f in features:
            countries.add(f["properties"]["name"])

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
    """Helper method average vaccine rate given a country"""
    df_country = df[df['location'] == country]
    avg_vax_rate = df_country["daily_vaccinations_per_million"].mean() / 1000000
    return avg_vax_rate


# ----------------------------------------------------------------------------------------------------------------------
# Testing
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    cont = pd.read_csv("datasets\\continents-according-to-our-world-in-data.csv")
    vac = pd.read_csv("datasets\\vaccinations.csv")
    pop = pd.read_csv("datasets\\population_by_country_2020.csv")
    count = _get_countries_on_map()
    countr = _get_all_countries(cont, vac, pop, count)
    print(str(len(countr)) + ": " + str(countr))

    vacr = _get_vaxrates(countr, vac)
    print(str(len(vacr)) + ": " + str(vacr))

    popu = _get_populations(countr, pop)
    print(str(len(popu)) + ": " + str(popu))

    exprate = _get_export_rates()
    print(str(len(exprate)) + ": " + str(exprate))

    shiptime = _get_shipment_times(countr)
    print(str(len(shiptime)) + ": " + str(shiptime))

    all_att = get_all_country_attributes()
    print(all_att)
