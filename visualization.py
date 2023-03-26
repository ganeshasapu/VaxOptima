# Draw a map using Folium
# Show each country on the map across generations

# Whenever you click on a country, reveal the popup for that country containing the graph with \
# its fitness value across generations (https://python-visualization.github.io/folium/quickstart.html, \
# https://nbviewer.org/github/python-visualization/folium/blob/main/examples/Popups.ipynb)

# Use Chloropleth to map each country, since it is compatible with Pandas. The colours represent the fitness \
# value of each country in the current generation.
# Use this json file for the borders and cite it \
# (https://github.com/python-visualization/folium/blob/main/examples/data/world-countries.json)

# For Styling, use the [16] red to yellow colour scheme \
# (https://python-visualization.github.io/folium/quickstart.html#Styling-function)


import json
import pandas as pd

import folium as folium
import requests as requests


def visualize_countries():
    countries = 'https://github.com/python-visualization/folium/blob/main/examples/data/world-countries.json'
    geo_json_data = json.loads(requests.get(countries).text)


def test_chloropleth():
    state_geo = 'https://github.com/python-visualization/folium/tree/main/examples/data/us-states.json'
    state_unemployment = \
        'https://github.com/python-visualization/folium/tree/main/examples/data/US_Unemployment_Oct2012.csv'
    state_data = pd.read_csv(state_unemployment)

    m = folium.Map(location=[48, -102], zoom_start=3)

    folium.Choropleth(
        geo_data=state_geo,
        name="choropleth",
        data=state_data,
        columns=["State", "Unemployment"],
        key_on="feature.id",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Unemployment Rate (%)",
    ).add_to(m)

    folium.LayerControl().add_to(m)
    m.render()
