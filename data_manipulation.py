"""File for manipulating for data in datasets folder"""
import pandas as pd
import geopandas as gp

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
    continent_df = pd.read_csv("datasets/continents-according-to-our-world-in-data.csv")
    vaccine_df = pd.read_csv("datasets/vaccinations.csv")
    population_df = pd.read_csv("datasets/population_by_country_2020.csv")
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
    """Helper Method that returns a dict mapping an exporting country to its population"""
    country_to_pop = {}
    for item in population_df.iterrows():
        country = item[1]['Country (or dependency)']
        population = item[1]['Population (2020)']
        if country in countries:
            country_to_pop[country] = population
    return country_to_pop


def _get_export_rates() -> dict:
    """Helper Method that returns a dict mapping a country to its export rate"""
    vac_exp = VACCINE_EXPORTERS
    country_vac_export_rate = {c: ((vac_exp[c] - 67000000) / (1986400000 - 67000000)) for c in vac_exp}
    return country_vac_export_rate


def _get_shipment_times(countries: dict) -> dict:
    """Helper Method that returns a dict mapping an exporter to its shipment time to different continents"""
    shipment_time = {c: VACCINE_SHIPMENT_TIME_CONTINENT[countries[c]] for c in VACCINE_EXPORTERS}
    return shipment_time


def _get_countries_on_map() -> set:
    """Helper Method that returns a set of countries that are represented on the folium map"""
    world = gp.read_file(gp.datasets.get_path("naturalearth_lowres"))

    # Reformatting certain country names
    world["name"].replace("United States of America", "United States", inplace=True)
    world["name"].replace("N. Cyprus", "North Cyprus", inplace=True)
    world["name"].replace("Falkland Is.", "Falkland Islands", inplace=True)
    world["name"].replace("Eq. Guinea", "Equitorial Guinea", inplace=True)
    world["name"].replace("Dem. Rep. Congo", "Democratic Republic of Congo", inplace=True)
    world["name"].replace("Central African Rep.", "Central African Republic", inplace=True)
    world["name"].replace("Dominican Rep.", "Dominican Republic", inplace=True)
    world["name"].replace("Soloman Is.", "Soloman Islands", inplace=True)
    world["name"].replace("S. Sudan", "South Sudan", inplace=True)
    world["name"].replace("Bosnia and Herz.", "Bosnia and Herzegovina", inplace=True)
    world["name"].replace("Timor-Leste", "Timor", inplace=True)
    world["name"].replace("Côte d'Ivoire", "Cote d'Ivoire", inplace=True)

    countries = world["name"].to_list()
    return set(countries)


def _get_avg_daily_vax_rate(df: pd.DataFrame, country: str) -> float:
    """Helper method average vaccine rate given a country"""
    df_country = df[df['location'] == country]
    avg_vax_rate = df_country["daily_vaccinations_per_million"].mean() / 1000000
    return avg_vax_rate


# ----------------------------------------------------------------------------------------------------------------------
# Testing
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ["pandas", "geopandas"],  # the names (strs) of imported modules
        'allowed-io': ["_get_countries_on_map"],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
