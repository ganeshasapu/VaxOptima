"""File for data manipulation for data in datasets folder"""
import pandas as pd

VACCINE_HESITANCY_RATE_CONTINENT = {"Asia": 0.15,
                                    "Europe": 0.25,
                                    "North America": 0.25,
                                    "South America": 0.15,
                                    "Oceania": 0.3,
                                    "Africa": 0.4}

VACCINE_EXPORTERS = {"Germany",
                     "Belgium",
                     "China",
                     "United States of America",
                     "South Korea",
                     "India",
                     "South Africa",
                     "Russia",
                     "Japan"}


def get_all_countries_shipment_time() -> dict[str: int]:
    """Returns a dictionary mapping a country to its vaccination shipment time"""


def get_all_countries_vaxhesitancy() -> dict[str: float]:
    """Returns a dictionary mapping a country to its vaccination hesitancy rate. Note that we generalize the vaccine
    hesitancy rate of each continent to each country due to lack of data"""
    countries = get_all_countries(_create_df("datasets\\vaccinations.csv"), "location", True)
    continent_df = _create_df("datasets\\continents-according-to-our-world-in-data.csv")
    country_vaxhesitacny = {}

    for item in continent_df.iterrows():
        country = item[1]['Entity']
        continent = item[1]['Continent']
        if country in countries:
            country_vaxhesitacny[country] = VACCINE_HESITANCY_RATE_CONTINENT[continent]
    return country_vaxhesitacny


def get_all_country_vaxrate() -> dict[str: float]:
    """Returns a dictionary mapping a country to its vaccination rate"""
    df = _create_df("datasets\\vaccinations.csv")
    countries = get_all_countries(df, "location", False)
    country_avg_vax_rate = {c: _get_avg_daily_vax_rate(df, c) for c in countries}
    return country_avg_vax_rate


def get_all_countries(df: pd.DataFrame, column_name: str, with_cont: bool) -> set | dict:
    """Get all countries given a data frame"""
    continent_df = _create_df("datasets\\continents-according-to-our-world-in-data.csv")
    countries_with_continents = set(continent_df["Entity"].unique())
    valid_countries = {c for c in set(df[column_name].unique()) if c in countries_with_continents}
    return valid_countries


# Helper Methods
def _create_df(file: str) -> pd.DataFrame:
    """Method to create data frame given csv file"""
    df = pd.read_csv(file)
    return df


def _get_avg_daily_vax_rate(df: pd.DataFrame, country: str) -> float:
    """Returns average vaccine rate given a country

    Preconditions:
        - dataframe includes column, "daily_vaccinations_per_million"
        - country name is formatted correctly
    """
    df_country = df[df['location'] == country]
    avg_vax_rate = df_country["daily_vaccinations_per_million"].mean() / 1000000
    return avg_vax_rate


if __name__ == "__main__":
    print(get_all_country_vaxrate())
