# Draw a map using Folium
# Show each country on the map across generations
import json


# Whenever you click on a country, reveal the popup for that country containing the graph with \
# its fitness value across generations (https://python-visualization.github.io/folium/quickstart.html, \
# https://nbviewer.org/github/python-visualization/folium/blob/main/examples/Popups.ipynb)

# Use Chloropleth to map each country, since it is compatible with Pandas. The colours represent the fitness \
# value of each country in the current generation.
# Use this json file for the borders and cite it \
# (https://github.com/python-visualization/folium/blob/main/examples/data/world-countries.json)

# For Styling, use the [16] red to yellow colour scheme \
# (https://python-visualization.github.io/folium/quickstart.html#Styling-function)



def visualize_countries():
    countries = 'https://github.com/python-visualization/folium/blob/main/examples/data/world-countries.json'
    geo_json_data = json.loads(requests.get(countries).text)
