# Draw a map using Folium
# Show each country on the map across generations
# Whenever you click on a country, reveal the popup for that country containing the graph with \
# its vaccination score across generations (https://python-visualization.github.io/folium/quickstart.html, \
# https://nbviewer.org/github/python-visualization/folium/blob/main/examples/Popups.ipynb)
# Use Chloropleth to map each country, since it is compatible with Pandas. The colours represent the vaccination score \
# of each country in the current generation.
# Use this json file for the borders and cite it \
# (https://github.com/python-visualization/folium/blob/main/examples/data/world-countries.json)

# For Styling, use the [16] red to yellow colour scheme \
# (https://python-visualization.github.io/folium/quickstart.html#Styling-function)
from urllib.request import urlopen

import pandas
import plotly.express as px
import geopandas

if __name__ == '__main__':
    data = {
        "Timestamp": ["2018-01-01", "2018-01-01", "2018-01-02", "2018-01-02"],
        "Country": ["United States", "Canada", "United States", "Canada"],
        "Vaccination_Score": [80, 60, 85, 70]
        }

    # Load data into a pandas DataFrame
    df = pandas.DataFrame(data)

    # Load a GeoDataFrame with world geometry data
    world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
    world["name"].replace("United States of America", "United States", inplace=True)

    # Merge your data with the GeoDataFrame
    world_data = world.merge(df, left_on="name", right_on="Country")
    countries = world["name"].tolist()
    print(countries)

    # Create the interactive map using plotly
    fig = px.choropleth(
        world_data,
        locations="iso_a3",
        color="Vaccination_Score",
        hover_name="Country",
        animation_frame="Timestamp",
        projection="natural earth",
        color_continuous_scale=px.colors.sequential.Plasma,
    )

    # Show the map
    fig.show()
