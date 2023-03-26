"""File for data manipulation for data in datasets folder"""
import pandas as pd


def create_df(file: str) -> pd.DataFrame:
    """Method to create data frame given csv file"""
    df = pd.read_csv(file)
    return df


def get_all_country_vaxrate() -> dict[str: float]:
    """Returns a dictionary mapping a country to its vaccination rate"""
    df = create_df("datasets\\vaccinations.csv")
    countries = get_all_countries(df)
    country_avg_vax_rate = {c: _get_avg_daily_vax_rate(df, c) for c in countries}
    return country_avg_vax_rate


def get_all_countries(df: pd.DataFrame) -> list:
    """Get all countries given a data frame"""
    return list(df["location"].unique())


# Helper Methods
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
