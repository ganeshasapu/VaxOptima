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

import pandas

import folium as folium

import ssl
import certifi
import os

import webbrowser

chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

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
    # Get the file csv file with country names and their vaccination scores, and pass it into pandas to extract the data
    countries_data = pandas.read_csv('countries_vaccination.csv')  # TODO: The file name is a placeholder

    # Initialize the world map and make its background black
    world_map = folium.Map(location=[48, -102], zoom_start=3)
    folium.TileLayer('cartodbdark_matter', name='Black Background', control=False).add_to(world_map)

    folium.Choropleth(
        geo_data=countries_geographical,
        name='choropleth',
        data=countries_data,
        columns=['Country', 'Vaccination Score'],
        key_on='feature.id',
        fill_color='RdYlGn',
        fill_opacity=0.9,
        line_opacity=0.2,
        smooth_factor=1,
        legend_name='Vaccination Score (TODO)',
    ).add_to(world_map)

    folium.LayerControl().add_to(world_map)
    world_map.save('visualization_result.html')
    webbrowser.get('chrome').open('visualization_result.html')


def test_chloropleth(layer_control: bool = False, black_bg: bool = False):
    """ This is just a test that displays an example Chloropleth map.
    We took this example from https://python-visualization.github.io/folium/quickstart.html and changed it around.
    """
    state_geo = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
    state_unemployment = \
        'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/US_Unemployment_Oct2012.csv'
    state_data = pandas.read_csv(state_unemployment)

    m = folium.Map(location=[48, -102], zoom_start=3)

    if black_bg:
        folium.TileLayer('cartodbdark_matter', name='Black Background', control=False).add_to(m)

    folium.Choropleth(
        geo_data=state_geo,
        name='choropleth1',
        data=state_data,
        columns=['State', 'Unemployment'],
        key_on='feature.id',
        fill_color='RdYlGn',
        fill_opacity=0.9,
        line_opacity=0.2,
        smooth_factor=1,
        legend_name='Unemployment Rate (%)',
    ).add_to(m)

    if layer_control:
        folium.Choropleth(
            geo_data=state_geo,
            name='choropleth2',
            data=state_data,
            columns=['State', 'Unemployment'],
            key_on='feature.id',
            fill_color='BrBG',
            fill_opacity=0.9,
            line_opacity=0.2,
            smooth_factor=1,
            legend_name='Unemployment Rate (%)',
        ).add_to(m)
        folium.LayerControl().add_to(m)

    # folium.Marker([30, -100], popup=folium.Popup('visualization_result.html')).add_to(m)

    # Define a style function to get rid of the blue lines
    def style_function(feature):
        return {
            "fillOpacity": 0,
            "weight": 0,
        }

    folium.GeoJson(
        data=state_geo, name='GeoJson',
        tooltip=folium.features.GeoJsonTooltip(fields=['name'], labels=False, sticky=True),
        style_function=style_function
    ).add_to(m)

    m.save('visualization_result.html')
    webbrowser.get('chrome').open('visualization_result.html')
