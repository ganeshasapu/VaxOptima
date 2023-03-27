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
import json
from typing import Any, Callable, Optional

import pandas

import folium as folium

import ssl
import certifi
import os

import webbrowser

# Preparation for browser display. We need to make sure we don't get an SSL error.
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['SSL_CERT_FILE'] = certifi.where()

def visualize_countries():
    """ Create a world map for the current generation with countries coloured in accordance with their vaccination scores.
    The greener a country appears, the higher its vaccination score is.
    The redder a country appears, the lower its vaccine score is.
    """
    # Get the geographical boundary data
    countries_geographical = \
        'https://raw.githubusercontent.com/python-visualization/folium/blob/main/examples/data/world-countries.json'
    # Get the csv file with country names and their vaccination scores, and pass it into pandas to extract the data
    countries_data, headers = generate_data('countries_vaccination.csv')

    # Initialize the world map and make its background black
    world_map = generate_map(background='black')

    # folium.Choropleth(
    #     geo_data=countries_geographical,
    #     name='choropleth',
    #     data=countries_data,
    #     columns=['Country', 'Vaccination Score'],
    #     key_on='feature.id',
    #     fill_color='RdYlGn',
    #     fill_opacity=0.9,
    #     line_opacity=0.2,
    #     smooth_factor=1,
    #     legend_name='Vaccination Score (TODO)',
    # ).add_to(world_map)

    add_choropleth(world_map, countries_geographical, countries_data, headers, 'Vaccination Score (TODO)',
                   key_on='feature.properties.name')
    # folium.LayerControl().add_to(world_map)

    display_map(world_map, 'visualization_result.html')


def test_chloropleth():
    """This is just a test that displays an example Chloropleth map.
    We looked at the example from https://python-visualization.github.io/folium/quickstart.html and reimplemented it in
    a way that is convenient to us.
    """
    state_geo = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
    state_data, headers = generate_data(
        'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/US_Unemployment_Oct2012.csv')
    m = generate_map(background='black')
    add_choropleth(m, state_geo, state_data, headers, 'Unemployment Rate (%)')
    add_geojson(m, state_geo)
    display_map(m, 'visualization_result.html')


# Our Helper Functions to Generate Maps More Easily
def display_map(folium_map: folium.Map, file: str) -> None:
    """Saves the generated map in the given file and displays the map on the web browser."""
    folium_map.save(file)
    webbrowser.open_new_tab('file://' + os.path.join(os.getcwd(), file))


def generate_data(link_or_dataframe: str | pandas.DataFrame, print_result: bool = False) -> tuple[
    pandas.DataFrame, list[str]]:
    """Extracts the dataframe from a github link if the input is not already a data frame.
    Returns a tuple containing the resultant dataframe and its headers.
    Prints the dataframe in the console if specified.
    """
    if isinstance(link_or_dataframe, str):
        data = pandas.read_csv(link_or_dataframe)
    else:
        data = link_or_dataframe
    if print_result:
        print(data)
    return (data, data.columns.tolist())


def generate_map(location: tuple = (48, -102), zoom_start: int = 3, background: str = '') -> folium.map:
    """Generates and returns a map object focused on the given coordinates with the given background.
    """
    background_options = {'black': 'cartodbdark_matter', 'white': 'cartodbpositron'}
    world_map = folium.Map(location=location, zoom_start=zoom_start)
    if background in background_options:
        folium.TileLayer(background_options[background], name='Background', control=False).add_to(world_map)
    return world_map


def add_choropleth(folium_map: folium.Map, geo_data: str, num_data: pandas.DataFrame, headers: list[str],
                   legend_name: str = '', colourbrew: str = 'RdYlGn', name: str = 'choropleth',
                   fill_opacity: float = 0.9, line_opacity: float = 0.2, smooth_factor: float = 1,
                   key_on: str = 'feature.id') -> None:
    """
    Generates a choropleth and adds it to the given map.
    """
    folium.Choropleth(
        geo_data=geo_data,
        name=name,
        data=num_data,
        columns=headers,
        key_on=key_on,
        fill_color=colourbrew,
        fill_opacity=fill_opacity,
        line_opacity=line_opacity,
        smooth_factor=smooth_factor,
        legend_name=legend_name,
    ).add_to(folium_map)


def add_geojson(folium_map: folium.Map, geo_data: str, name: str = 'GeoJSON',
                fields: list[str] = ['name'],
                labels: bool = False, sticky: bool = True):
    """
    Generates a GeoJSON and adds it to the given map.
    The style function is used to prevent thick blue borders.
    """

    def style_function(feature):
        return {
            "fillOpacity": 0,
            "weight": 0,
        }

    folium.GeoJson(
        data=geo_data, name=name,
        tooltip=folium.features.GeoJsonTooltip(fields=fields, labels=labels, sticky=sticky),
        style_function=style_function
    ).add_to(folium_map)
