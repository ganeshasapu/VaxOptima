import os
from urllib.request import urlopen
import webbrowser

import pandas
import plotly.express as px
import geopandas
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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

    # Merge your data with the GeoDataFrame
    world_data = world.merge(dataframe, left_on="name", right_on="Country")

    custom_color_scale = [
        (0, "#ff0000"),
        (0.5, "#ffff00"),
        (1.0, "#00ff00"),
    ]

    # Create the interactive map using plotly
    cloropleth = px.choropleth(
        world_data,
        locations="iso_a3",
        color="Percent Vaccinated",
        hover_name="Country",
        animation_frame="Timestamp",
        projection="natural earth",
        color_continuous_scale=custom_color_scale,
        range_color=(0.0, 1.0)
    )

    cloropleth.write_html("world_map.html")
    os.system("open world_map.html")


def visualize_fitness(fitness_values : pandas.DataFrame):
    """
    Visualize the fitness values over time.
    """
    line_graph = px.line(fitness_values, x="Timestamp", y="Fitness Value", title="Fitness over time")

    line_graph.write_html("fitness.html")
    os.system("open fitness.html")