# Draw a map using Folium
# Show each country on the map across generations
# Whenever you click on a country, reveal the popup for that country containing the graph with \
# its vaccination score across generations (https://python-visualization.github.io/folium/quickstart.html, \
# https://nbviewer.org/github/python-visualization/folium/blob/main/examples/Popups.ipynb)
import datetime
# Use Chloropleth to map each country, since it is compatible with Pandas. The colours represent the vaccination score \
# of each country in the current generation.
# Use this json file for the borders and cite it \
# (https://github.com/python-visualization/folium/blob/main/examples/data/world-countries.json)

# For Styling, use the [16] red to yellow colour scheme \
# (https://python-visualization.github.io/folium/quickstart.html#Styling-function)
import json
import random
import time
from urllib.request import urlopen

import branca
from branca.colormap import LinearColormap
import numpy
import pandas
import folium
import ssl
import os
import webbrowser
import requests
import folium.plugins

# Disable SSL verification, since it can prevent the web browser tabs from opening
ssl._create_default_https_context = ssl._create_unverified_context


def visualize_countries():
    """ Create a world map for the current generation with countries coloured in accordance with their vaccination scores.
    The greener a country appears, the higher its vaccination score is.
    The redder a country appears, the lower its vaccine score is.
    """
    # Get the geographical boundary data
    countries_geographical = \
        'https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json'
    # Get the csv file with country names and their vaccination scores, and pass it into pandas to extract the data
    countries_data, headers = generate_data('visualization_data/placeholder.csv', True)
    # Initialize the world map and make its background black
    world_map = generate_map(background='terrain')
    add_choropleth(world_map, countries_geographical, countries_data, headers, 'GDP (current US$) - 2020',
                   key_on='feature.properties.name')
    display_map(world_map, 'visualization_result.html')


def test_choropleth():
    """This is just a test that displays an example Choropleth map.
    We looked at the example from https://python-visualization.github.io/folium/quickstart.html and reimplemented it in
    a way that is convenient to us.
    """
    state_geo = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
    state_data, headers = generate_data(
        'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/US_Unemployment_Oct2012.csv')
    m = generate_map(background='terrain')
    add_choropleth(m, state_geo, state_data, headers, 'Unemployment Rate (%)', key_on='feature.id')
    add_geojson(m, state_geo)
    display_map(m, 'visualization_result.html')


# def test_world_map1():
#     """
#     We have played around with the example from
#     https://stackoverflow.com/questions/63613032/how-to-draw-a-world-map-in-folium-and-indicate-some-countries-on-it
#     to test whether the world map visualization is working.
#     """
#     # dynamically get the world-country boundaries
#     # We have a cleaner way of extracting data
#     res = requests.get(
#         "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json")
#     df = pandas.DataFrame(json.loads(res.content.decode()))
#     df = df.assign(id=df["features"].apply(pandas.Series)["id"],
#                    name=df["features"].apply(pandas.Series)["properties"].apply(pandas.Series)["name"])
#
#     # build a dataframe of country colours scraped from wikipedia
#     # We are not going to use anything of this sort, so we can just ignore this part
#     resp = requests.get("https://en.wikipedia.org/wiki/National_colours", )
#     soup = BeautifulSoup(resp.content.decode(), "html.parser")
#     colours = []
#     for t in soup.find_all("table", class_="wikitable"):
#         cols = t.find_all("th")
#         ok = (len(cols) > 5 and cols[0].string.strip() == "Country" and cols[4].string.strip() == "Primary")
#         if ok:
#             for tr in t.find_all("tr"):
#                 td = tr.find_all("td")
#                 if len(td) > 5:
#                     sp = td[4].find_all("span")
#                     c1 = re.sub("background-color:([\w,#,0-9]*).*", r"\1", sp[0]["style"])
#                     c2 = c1 if len(sp) == 1 else re.sub("background-color:([\w,#,0-9]*).*", r"\1", sp[1]["style"])
#                     colours.append({"country": td[0].find("a").string,
#                                     "colour1": c1,
#                                     "colour2": c2,
#
#                                     })
#     dfc = pandas.DataFrame(colours).set_index("country")
#
#     # Let's see what the dataframe is
#     print(dfc)
#
#     # a list of interesting countries - Singapore is missing!
#     # I have added Turkey, and it shows up!
#     countries = ['Singapore', 'Malaysia', 'Indonesia', 'Vietnam', 'Philippines', 'Turkey']
#
#     # style the overlays with the countries own colors...
#     # We have our own style function, so ignore this part
#     def style_fn(feature):
#         cc = dfc.loc[feature["properties"]["name"]]
#         ss = {'fillColor': f'{cc[0]}', 'color': f'{cc[1]}'}
#         return ss
#
#     # create the base map
#     # We have changed this to our own helper function
#     m = generate_map(location=(1.34, 103.82), zoom_start=6, background='terrain')
#
#     # overlay desired countries over folium map
#     # We are going to use a Choropleth instead of GeoJSON; still, understanding this part helps.
#     for r in df.loc[df["name"].isin(countries)].to_dict(orient="records"):
#         folium.GeoJson(r["features"], name=r["name"], tooltip=r["name"], style_function=style_fn).add_to(m)
#
#     # We have added this to visualize the map on our browser
#     display_map(m, 'visualization_result.html')  # Thankfully, it works!


def test_world_map2():
    """
    This is our attempt at creating a test for our world map visualization, using pretend data.
    This is not a good method of testing though, since there is a huge difference between numbers.
    At least, this was our first successful attempt of verifying our map visualization.
    """
    # Here we get the geographical data
    countries_geographical = \
        'https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json'

    # Here we extract the dataframe, modify it, and assign the headers
    df = pandas.read_csv('visualization_data/area_example.csv', skiprows=4)
    df = df.loc[:, ['Country Name', '2020']]
    df = df.rename(columns={'Country Name': 'Country', '2020': 'Area'})
    print(df)
    headers = ['Country', 'Area']

    # Generate the map
    world_map = generate_map(background='terrain')

    # Add the Choropleth
    add_choropleth(world_map, countries_geographical, df, headers, legend_name='Area', key_on='feature.properties.name')

    # Display the map
    display_map(world_map, 'visualization_result.html')


def test_world_map3():
    """
    In this test, we can use a pretend dataframe we generate instead of an actual csv file. Let's see how it goes!
    """
    # Get the geographical border data
    countries_geographical = \
        'https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json'

    # Generate a pretend dataframe with each country having a random vaccination score 0.0-1.0
    countries = ['Turkey', 'Syria', 'India', 'United States of America']
    headers = ['Country', 'Vaccination Score']
    dataframe = pandas.DataFrame(
        {'Country': countries, 'Vaccination Score': numpy.random.uniform(0.0, 1.0, len(countries))})
    print(dataframe)

    # Generate the map
    world_map = generate_map(background='terrain')

    # Add the Choropleth
    add_choropleth(world_map, countries_geographical, dataframe, headers, legend_name='Vaccination Score',
                   key_on='feature.properties.name')

    # Display the map
    display_map(world_map, 'visualization_result.html')


def test_world_map4(countries: int):
    """
    In this test, we have fully automated the example dataframe generation.
    The only input is the number of countries we want in our visualization.
    """
    # Get the geographical border data
    countries_geographical = \
        'https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json'

    # Generate the example dataframe and its headers
    dataframe, headers = generate_example_dataframe(countries, countries_geographical, (0.0, 1.0), print_result=True)

    # Generate the map
    world_map = generate_map(background='terrain')

    # Add the Choropleth
    add_choropleth(world_map, countries_geographical, dataframe, headers, legend_name='Vaccination Score',
                   key_on='feature.properties.name')

    # Display the map
    display_map(world_map, 'visualization_result.html')


def test_world_map5(runs: int, int_range: tuple[int, int] | int):
    """
    This is the ultimate example dataframe test.
    This test runs test_world_map4 a specified number of times with a specified number/range of countries.
    """
    # Run the specified number of times
    for _ in range(0, runs):
        if isinstance(int_range, tuple):  # Generate a random integer within the specified range
            countries = random.randint(int_range[0], int_range[1])
        else:  # Otherwise, use the given int
            countries = int_range
        test_world_map4(countries)


def isolate_timestamp(timestamp: int, dataframe: pandas.DataFrame):
    """
    After running the simulation, pass the desired timestamp and the resultant dataframe into this function to visualize
    the data in the given timestamp.
    """
    countries_geographical = \
        'https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json'
    num_data = dataframe[dataframe['Timestamp'] == timestamp].drop('Timestamp', axis=1)
    headers = num_data.columns.tolist()
    world_map = generate_map(background='terrain')
    add_choropleth(world_map, countries_geographical, num_data, headers, legend_name=num_data.columns.tolist()[1],
                   key_on='feature.properties.name')
    display_map(world_map, 'visualization_result.html')


def isolate_timestamp_and_display(dataframe: pandas.DataFrame):
    timestamps = dataframe['Timestamp']
    for i in range(min(timestamps), max(timestamps) + 1):
        isolate_timestamp(i, dataframe)


def test_isolation():
    # Create list of country names
    countries = ['USA', 'Canada', 'UK', 'France', 'Germany', 'Australia', 'Japan', 'Brazil', 'Russia', 'China']

    # Create empty dataframe
    dataframe = pandas.DataFrame(columns=['Timestamp', 'Country', 'Percent Vaccinated'])

    # Populate dataframe with random values
    for ts in range(10):
        for country in countries:
            percent_vaccinated = round(random.uniform(0, 1), 2)
            dataframe = dataframe.append({'Timestamp': ts, 'Country': country, 'Percent Vaccinated': percent_vaccinated},
                           ignore_index=True)

    isolate_timestamp_and_display(dataframe)

# def test_multiple_timestamps():
#     df = pandas.DataFrame({
#         'Timestamp': ['2022-01-01', '2022-01-01', '2022-01-02', '2022-01-02'],
#         'Country': ['USA', 'Canada', 'USA', 'Canada'],
#         'Vaccination Score': [80, 60, 85, 70]
#     })
#
#     df['Timestamp'] = pandas.to_datetime(df['Timestamp'])
#     dt_index_epochs = df['Timestamp'].astype(int) // 10 ** 9
#     df['Timestamp'] = dt_index_epochs
#
#     color_scale = branca.colormap.LinearColormap(
#         colors=['#d73027', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850'],
#         vmin=df['Vaccination Score'].min(),
#         vmax=df['Vaccination Score'].max(),
#         caption='Vaccination Score',
#     )
#
#     world_map = generate_map(background='terrain')
#
#     # Read in GeoJSON data
#     url = 'https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json'
#     response = requests.get(url)
#     geojson_data = json.loads(response.content.decode())
#
#     # Create a dictionary to map country names to vaccination scores
#     country_vaccination_scores = dict(zip(df['Country'], df['Vaccination Score']))
#
#     # Initialize feature variable
#     feature = None
#
#     # Iterate over each feature in the GeoJSON data and add a new 'Vaccination Score' property
#     # based on the corresponding vaccination score for the country
#     for feature in geojson_data['features']:
#         country_name = feature['properties']['name']
#         if country_name in country_vaccination_scores:
#             vaccination_score = country_vaccination_scores[country_name]
#             feature['properties']['Vaccination Score'] = vaccination_score
#         else:
#             feature['properties']['Vaccination Score'] = None
#
#     folium.plugins.TimeSliderChoropleth(
#         data=json.dumps(geojson_data),
#         styledict={
#             str(timestamp): {
#                 'fillColor': '#ff0000' if feature is None or feature['properties'][
#                     'Vaccination Score'] is None else color_scale(
#                     feature['properties']['Vaccination Score']),
#                 'color': '#000000',
#                 'weight': 1,
#                 'fillOpacity': 0.7
#             }
#             for timestamp in df['Timestamp'].unique()
#         },
#         overlay=True,
#         name='Vaccination Scores',
#         control=True,
#         show=False,
#         init_timestamp=0
#     ).add_to(world_map)
#
#     display_map(world_map, 'visualization_result.html')


# Our Helper Functions for Generating Example Test Data
def generate_example_dataframe(countries: int, geodata: str, float_range: tuple[float, float],
                               fitness_name: str = 'Vaccination Score', print_result: bool = False) -> tuple[
    pandas.DataFrame, list[str]]:
    """
    This function is used for generating example test data.
    Extracts the specified amount of country names from the given link. Then assigns each country a random fitness value
    in the specified range (lowerbound, upperbound).
    Returns the resultant DataFrame and its headers.
    Prints the resultant DataFrame if specified.
    """
    # Sample a specified number of country names from the geodata link
    country_names = random.sample \
        ([country['properties']['name'] for country in requests.get(geodata).json()['features']], countries)

    # Generate the dataframe with the selected countries and their random fitness values in the given range
    lowerbound, upperbound = float_range
    dataframe = pandas.DataFrame(
        {'Country': country_names, fitness_name: numpy.random.uniform(lowerbound, upperbound, len(country_names))})

    # Prints the dataframe if specified (also its length for testing purposes)
    if print_result:
        print(dataframe)
        print('Length: ' + str(len(country_names)))

    # Returns the dataframe
    return (dataframe, dataframe.columns.tolist())


# Our Helper Functions to Generate Maps More Easily
def display_map(folium_map: folium.Map, file: str) -> None:
    """Saves the generated map in the given file and displays the map on the web browser."""
    # Save the html info into the file and generate a website path for it
    folium_map.save(file)
    website = 'file://' + os.path.join(os.getcwd(), file)

    # Open the web browser tab to display the map
    webbrowser.open_new_tab(website)


def generate_data(link_or_dataframe: str | pandas.DataFrame, print_result: bool = False) \
        -> tuple[pandas.DataFrame, list[str]]:
    """Extracts the DataFrame from a link unless the input is already a DataFrame.
    Returns a tuple containing the resultant DataFrame and its headers.
    Prints the DataFrame in the console if specified.
    """
    if isinstance(link_or_dataframe, str):  # Extract the DataFrame if given a link
        if link_or_dataframe.endswith('.csv'):  # The link is for a csv file
            data = pandas.read_csv(link_or_dataframe)
        else:  # Otherwise read html (We won't need this, but it's good to have)
            data = pandas.read_html(link_or_dataframe)
    else:  # The data is already a DataFrame
        data = link_or_dataframe

    # Print the resultant DataFrame if specified
    if print_result:
        print(data)

    # Return the tuple containing the DataFrame and its headers.
    return (data, data.columns.tolist())


def generate_map(location: tuple = (48, -102), zoom_start: int = 3, background: str = '') -> folium.map:
    """Generates and returns a map object focused on the given coordinates with the given background.
    """
    # Define a dict containing all the background colour options
    background_options = {'black': 'cartodbdark_matter', 'white': 'cartodbpositron', 'terrain': 'stamenterrain',
                          'monochromatic': 'stamentoner'}

    # Initialize the map object
    world_map = folium.Map(location=location, zoom_start=zoom_start)

    # If a valid background colour is passed into the function, change the background to it
    if background in background_options:
        folium.TileLayer(background_options[background], name='Background', control=False).add_to(world_map)

    # Return the map object
    return world_map


def add_choropleth(folium_map: folium.Map, geo_data: str, num_data: pandas.DataFrame, headers: list[str],
                   legend_name: str = '', colourbrew: str = 'RdYlGn', name: str = 'choropleth',
                   fill_opacity: float = 0.9, line_opacity: float = 0.2, smooth_factor: float = 1,
                   key_on: str = 'feature.properties.name') -> None:
    """
    Generates a Choropleth and adds it to the given map.
    Creates a TimeSliderChoropleth if time_slider is True.
    """

    # To prevent a JSON error, we convert the link to proper json
    geo_data_json = json.loads(requests.get(geo_data).content.decode('utf-8'))

    # Add the Choropleth object
    folium.Choropleth(
        geo_data=geo_data_json,
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
    """

    # Define a style function to prevent the default blue GeoJSON borders
    def style_function(feature):
        return {
            "fillOpacity": 0,
            "weight": 0,
        }

    # Initialize and add the GeoJSON object
    folium.GeoJson(
        data=geo_data, name=name,
        tooltip=folium.features.GeoJsonTooltip(fields=fields, labels=labels, sticky=sticky),
        style_function=style_function
    ).add_to(folium_map)
