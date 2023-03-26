import pandas as pd
"""File for data manipulation for data in datasets folder"""

def create_df(file: str) -> pd.DataFrame:
    """Method to create data frame given csv file"""
    df = pd.read_csv(file)


def get_all_countries(df: pd.DataFrame):
    return df["location"].unique()


def get_avg_daily_vax_rate(df: pd.DataFrame, country: str) -> float:
    """Returns average vaccine rate given a country

    Preconditions:
        - dataframe includes column, "daily_vaccinations_per_million"
        - country name is formatted correctly
    """
    df_country = df.query("location == country")
    avg_vax_rate = df_country["daily_vaccinations_per_million"].mean() / 1000000
    return avg_vax_rate


if __name__ == "__main__":
    df = create_df("datasets\\vaccinations.csv")
    countries = get_all_countries(df)
    print(countries)
    avg_vax_rate = [get_avg_daily_vax_rate(df, c) for c in countries]
    print(avg_vax_rate)


