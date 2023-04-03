from urllib.request import urlopen

import pandas
import plotly.express as px
import geopandas

def visualize_data(dataframe : pandas.DataFrame):
    """
    Visualize the dataframe on a map across timestamps using plotly and geopandas.
    """
    # Load a GeoDataFrame with world geometry data
    world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
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
    print(set(countries))


    # Merge your data with the GeoDataFrame
    world_data = world.merge(dataframe, left_on="name", right_on="Country")

    custom_color_scale = [
        (0, "#ff0000"),
        (0.5, "#ffff00"),
        (1.0, "#00ff00"),
    ]

    # Create the interactive map using plotly
    fig = px.choropleth(
        world_data,
        locations="iso_a3",
        color="Percent Vaccinated",
        hover_name="Country",
        animation_frame="Timestamp",
        projection="natural earth",
        color_continuous_scale=custom_color_scale,
        range_color=(0.0, 1.0)
    )

    # Show the map
    fig.show()

if __name__ == '__main__':
    data = pandas.DataFrame({
        "Timestamp": [1, 1, 1, 2, 2, 2],
        "Country": ["United States", "Canada", 'Mexico', "United States", "Canada", 'Mexico'],
        "Percent Vaccinated": [20, 50, 30, 50, 70, 100]
        })
    visualize_data(data)

    # # Load data into a pandas DataFrame
    # df = pandas.DataFrame(data)

    # # Load a GeoDataFrame with world geometry data
    # world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
    # world["name"].replace("United States of America", "United States", inplace=True)

    # # Merge your data with the GeoDataFrame
    # world_data = world.merge(df, left_on="name", right_on="Country")
    # countries = world["name"].tolist()
    # print(countries)

    # # Create the interactive map using plotly
    # fig = px.choropleth(
    #     world_data,
    #     locations="iso_a3",
    #     color="Vaccination_Score",
    #     hover_name="Country",
    #     animation_frame="Timestamp",
    #     projection="natural earth",
    #     color_continuous_scale=px.colors.sequential.Plasma,
    # )

    # # Show the map
    # fig.show()
